import logging
import json
import os
import asyncio
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from userUtils.user_utils import get_current_user
from aiModel.ai_therapist import (
    feelings_analysis_agent,
    stream_emotional_therapist_agent,
    emotional_therapist_agent,
    summary_agent,
    analyze_agent,
    title_agent,
)
from redisCache.redis_cache import get_cache, set_cache, reset_cache
from .utils import (
    save_conversation_entry,
    get_conversational_entries,
    delete_conversational_entry,
    get_current_time,
    get_user_journal_stats,
    save_test_conversation_entry,
    save_conversation_logs,
    update_user_subscription,
    cancel_user_subscription,
    get_user_account_details,
    get_test_user_entries,
)
from database_init import get_db_connection
from models.conversational_history import ConversationalHistory
from time import perf_counter

router = APIRouter()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@router.post("/stream-ai-prompt")
def stream_ai_prompt(request: dict, token: str = Depends(get_current_user)):
    user_name = token["user_metadata"]["name"]
    user_message = request.get("user_message")
    conversation_history = request.get("conversation_history")
    completion = emotional_therapist_agent(
        user_message, conversation_history, user_name
    )
    # Save conversation logs
    return StreamingResponse(
        stream_emotional_therapist_agent(completion), media_type="text/plain"
    )


@router.get("/create-payment-intent")
async def create_payment_intent(token: str = Depends(get_current_user)):
    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=499,  # $4.99 in cents
            currency="usd",
            automatic_payment_methods={
                "enabled": True,
            },
        )
        return {"clientSecret": payment_intent.client_secret}

    except Exception as e:
        logging.error("Failed to create payment intent: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/get-user-account-details")
async def get_user_account_details_route(
    token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)
):
    user_id = token["sub"]
    if user_id == "1f2aa95c-e667-4476-8d67-5f92b5de1d7b":
        return "test user"
    account_details = await get_user_account_details(db_connection, user_id)
    logging.info("User account details: %s", account_details)
    return account_details


@router.post("/stripe-webhook")
async def stripe_webhook(
    request: Request,
    db_connection=Depends(get_db_connection),
):
    try:
        logging.info("Webhook received")
        stripe_signature = request.headers.get("stripe-signature")
        logging.info("Stripe signature: %s", stripe_signature)

        payload = await request.body()
        logging.info("Webhook payload received: %s", payload.decode())

        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        try:
            event = stripe.Webhook.construct_event(
                payload, stripe_signature, webhook_secret
            )
            logging.info("Event constructed successfully: %s", event.type)
        except ValueError as e:
            logging.error("Invalid payload error: %s", str(e))
            raise HTTPException(status_code=400, detail="Invalid payload") from e
        except stripe.error.SignatureVerificationError as e:
            logging.error("Signature verification error: %s", str(e))
            raise HTTPException(status_code=400, detail="Invalid signature") from e

        # Handle the event
        if event.type == "customer.subscription.updated":
            subscription = event.data.object
            logging.info("Subscription status: %s", subscription.status)

            customer = stripe.Customer.retrieve(subscription.customer)
            user_id = customer.metadata.get("user_id")
            if not user_id:
                logging.error("User ID not found in metadata")
                raise HTTPException(
                    status_code=400, detail="User ID not found in metadata"
                )
            logging.info("User ID: %s", user_id)
            logging.info("Subscription status: %s", subscription.status)

            if subscription.status == "active":
                # Update subscription when payment is successful
                current_period_end = subscription.current_period_end
                subscription_id = subscription.id
                update_user_subscription(
                    db_connection, user_id, current_period_end, subscription_id
                )
            elif subscription.status in ["incomplete_expired", "canceled", "unpaid"]:
                # Cancel subscription for failed/cancelled payments
                current_period_end = subscription.current_period_end
                cancel_user_subscription(db_connection, user_id, current_period_end)

        elif event.type == "customer.subscription.deleted":
            subscription = event.data.object

            customer = stripe.Customer.retrieve(subscription.customer)
            user_id = customer.metadata.get("user_id")
            if not user_id:
                logging.error("User ID not found in metadata")
                raise HTTPException(
                    status_code=400, detail="User ID not found in metadata"
                )
            logging.info("User ID: %s", user_id)
            logging.info("Subscription status: %s", subscription.status)
            current_period_end = subscription.current_period_end
            cancel_user_subscription(db_connection, user_id, current_period_end)

        return {"status": "success"}

    except Exception as e:
        logging.error("Error processing webhook: %s", str(e))
        db_connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to process webhook") from e


@router.post("/cancel-subscription")
async def cancel_subscription(
    request: dict,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
):
    try:
        user_id = token["sub"]

        if "subscription_id" not in request:
            raise HTTPException(status_code=400, detail="Subscription ID is required")

        subscription_id = request["subscription_id"]

        subscription = stripe.Subscription.retrieve(subscription_id)
        stripe.Subscription.modify(subscription_id, cancel_at_period_end=True)
        current_period_end = subscription.current_period_end
        cancel_user_subscription(db_connection, user_id, current_period_end)
        return {
            "message": "Subscription successfully canceled",
            "status": subscription.status,
        }

    except stripe.error.StripeError as e:
        logging.error("Stripe error while canceling subscription: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error("Error canceling subscription: %s", str(e))
        db_connection.rollback()
        raise HTTPException(status_code=500, detail="Failed to cancel subscription")


@router.post("/create-subscription")
async def create_subscription(
    request: dict,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
):
    try:
        user_email = token["email"]
        user_id = token["sub"]

        user_stats = get_user_journal_stats(db_connection, user_id)

        if user_stats["is_subscribed"] and not user_stats.get("subscription_end_date"):
            raise HTTPException(
                status_code=400, detail="You already have an active subscription"
            )

        if "payment_method_id" not in request:
            raise HTTPException(status_code=400, detail="Payment method ID is required")

        payment_method_id = request["payment_method_id"]
        current_time = get_current_time("UTC")

        existing_customers = stripe.Customer.list(email=user_email)
        if existing_customers and existing_customers.data:
            stripe_customer = existing_customers.data[0]

            stripe.Customer.modify(
                stripe_customer.id,
                payment_method=payment_method_id,
                invoice_settings={"default_payment_method": payment_method_id},
                metadata={
                    "user_id": user_id,
                    "subscription_start_date": current_time,
                    "user_email": user_email,
                },
            )
        else:

            stripe_customer = stripe.Customer.create(
                email=user_email,
                name="User Subscription",
                payment_method=payment_method_id,
                metadata={
                    "user_id": user_id,
                    "subscription_start_date": current_time,
                    "user_email": user_email,
                },
                invoice_settings={"default_payment_method": payment_method_id},
            )

        product = stripe.Product.create(name="Premium Subscription")
        price = stripe.Price.create(
            product=product.id,
            unit_amount=499,
            currency="usd",
            recurring={"interval": "month"},
        )

        subscription = stripe.Subscription.create(
            customer=stripe_customer.id,
            items=[{"price": price.id}],
            default_payment_method=payment_method_id,
        )

        current_period_end = subscription.current_period_end

        update_user_subscription(
            db_connection, user_id, current_period_end, subscription.id
        )

        return {
            "subscription_id": subscription.id,
            "status": subscription.status,
            "current_period_end": current_period_end,
        }

    except stripe.error.AuthenticationError as e:
        logging.error("Stripe authentication failed: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to authenticate with Stripe"
        ) from e
    except stripe.error.CardError as e:
        logging.error("Card error: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logging.error("Failed to create subscription: %s", str(e))
        raise HTTPException(
            status_code=500, detail="Failed to create subscription"
        ) from e


@router.delete("/refresh-convo-session")
async def refresh_convo_session(token: str = Depends(get_current_user)):
    user_id = token["sub"]
    reset_cache(user_id)
    return {"message": "Conversation session refreshed successfully"}


@router.put("/update-convo-session")
async def update_convo_session(
    request: dict,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
):
    user_id = token["sub"]
    conversation_history = request.get("conversation_history")
    if conversation_history and len(conversation_history) > 0:
        last_conversation = conversation_history[-1]
        user_message = last_conversation.get("user", "")
        therapist_response = last_conversation.get("therapist", "")

        logging.info("User message: %s", user_message)
        logging.info("Therapist response: %s", therapist_response)
        save_conversation_logs(db_connection, user_message, therapist_response)
    return {"message": "Conversation session updated successfully"}



async def check_subscription_limit(
    token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)
):
    user_id = token["sub"]
    journal_stats = get_user_journal_stats(db_connection, user_id)
    entries_this_month = journal_stats["entries_this_month"]
    is_subscribed = journal_stats["is_subscribed"]

    if not is_subscribed and entries_this_month >= 5:
        raise HTTPException(
            status_code=403,
            detail="You have exceeded the free tier limit of 5 entries per month. Please subscribe to continue using the service.",
        )
    return True


@router.post("/save-convo-entry")
async def save_convo_entry(
    conversational_history: ConversationalHistory,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
    _=Depends(check_subscription_limit),
):
    try:
        timezone = conversational_history.timezone
        logging.info("timezone: %s", timezone)
        current_time = get_current_time(timezone)
        user_id = token["sub"]
        user_name = token["user_metadata"]["name"]
        start_time = perf_counter()
        converse_history = conversational_history.conversation_history

        summary_task = summary_agent(converse_history, user_name)
        analysis_task = analyze_agent(converse_history, user_name)
        title_task = title_agent(converse_history)
        emotional_task = feelings_analysis_agent(converse_history)
        summary, analysis, title, emotions = await asyncio.gather(
            summary_task, analysis_task, title_task, emotional_task
        )

        # Save journal entry based on user type
        if user_id == "1f2aa95c-e667-4476-8d67-5f92b5de1d7b":
            journal_id = save_test_conversation_entry(
                db_connection, title, summary, analysis, emotions, current_time, user_id
            )
        else:
            journal_id = save_conversation_entry(
                db_connection, user_id, title, summary, analysis, emotions, current_time
            )

        end_time = perf_counter()
        elapsed_time = end_time - start_time
        logging.info("Time taken to save conversation entry: %s", elapsed_time)
        logging.info("Journal saved successfully with id of %s", journal_id)
        return {
            "title": title,
            "summary": summary,
            "analysis": analysis,
            "emotions": emotions.get("emotions"),
            "results": f"Journal saved successfully with id of {journal_id}",
        }

    except Exception as e:
        logging.error("Failed to save conversation entry: %s", e)
        raise


@router.get("/conversational-entries")
async def get_all_conversational_entries(
    token: str = Depends(get_current_user), db_connection=Depends(get_db_connection)
):
    try:
        user_id = token["sub"]
        if user_id == "1f2aa95c-e667-4476-8d67-5f92b5de1d7b":
            entries = get_test_user_entries(db_connection, user_id)
            user_id = "test_user"
            return {
                "entries": entries,
                "is_subscribed": False,
                "entries_this_month": 0,
                "user_id": user_id,
            }
        entries = get_conversational_entries(db_connection, user_id)
        stats = get_user_journal_stats(db_connection, user_id)

        return {
            "entries": entries,
            "is_subscribed": stats["is_subscribed"],
            "entries_this_month": stats["entries_this_month"],
            "user_id": user_id,
        }
    except Exception as e:
        logging.error("Failed to get conversational entries: %s", e)
        raise


@router.delete("/delete-convo-entry/{journal_id}")
async def delete_convo_entry(
    journal_id: str,
    token: str = Depends(get_current_user),
    db_connection=Depends(get_db_connection),
):
    try:
        user_id = token["sub"]
        logging.info("Deleting journal entry with id: %s", journal_id)
        delete_conversational_entry(db_connection, journal_id)
        entries = get_conversational_entries(db_connection, user_id)
        return {"entries": entries}
    except Exception as e:
        logging.error("Failed to delete journal entry: %s", e)
        raise

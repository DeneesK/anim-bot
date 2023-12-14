from aiogram import types

from src.tgbot.analysis.amplitude import amp
from src.settings.logger import logger
from src.settings.const import EVENTS


async def send_and_log(event_name, id,
                       event_properties=None,
                       user_properties=None):
    try:
        await amp.log(id, event_name,
                      event_properties=event_properties,
                      user_properties=user_properties)
        logger.info(f"id: {id},\n"
                    f"event_name: {event_name},\n"
                    f"event_properties: {event_properties},\n"
                    f"user_properties: {user_properties}\n")
    except Exception as error:
        logger.error(f"Error: {error}")


async def amplitude_registration(message):
    event_name = "registration"
    user_properties = {"username": message.from_user.username,
                       "first_name": message.from_user.first_name,
                       "last_name": message.from_user.last_name}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def ref_reg(message: types.Message,
                  userid_referral: int) -> None:
    event_name = EVENTS.get('ref_reg')
    user_properties = {'user_id': message.from_user.id,
                       'userid_referral': userid_referral}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def organic_reg(message: types.Message,
                      userid_referral: int) -> None:
    event_name = 'Organic regestration'
    user_properties = {'user_id': message.from_user.id,
                       'userid_referral': userid_referral}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def amplitude_error(message, text_error,
                          event_name="error",
                          question_type="text"):
    if event_name != "error":
        event_name = "error_" + event_name
    event_properties = {"error": text_error,
                        "question": message.text,
                        "question_type": question_type}
    user_properties = {"username": message.from_user.username,
                       "first_name": message.from_user.first_name,
                       "last_name": message.from_user.last_name}
    await send_and_log(event_name, message.from_user.id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def amplitude_wrong_content(message):
    event_name = "wrong_conten_type"
    event_properties = {"content_type": message.content_type}
    user_properties = {"username": message.from_user.username,
                       "first_name": message.from_user.first_name,
                       "last_name": message.from_user.last_name}
    await send_and_log(event_name, message.from_user.id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def user_start(message: types.Message) -> None:
    event_name = EVENTS.get('start')
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def user_singup(message: types.Message) -> None:
    event_name = EVENTS.get('singup')
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def user_sent_photo(message: types.Message) -> None:
    event_name = 'user sent photo'
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def user_save_to_db(message: types.Message, group: str) -> None:
    event_name = EVENTS.get('save_to_db')
    user_properties = {'user_id': message.from_user.id,
                       'group': group}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def api_request(message: types.Message):
    event_name = EVENTS.get('req_')
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def api_resp(message: types.Message, gen_time: int):
    event_name = EVENTS.get('resp_')
    event_properties = {'generationTime': gen_time}
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       event_properties=event_properties,
                       user_properties=user_properties)


async def sent_result(message: types.Message,):
    event_name = EVENTS.get('sent_result')
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def sent_to_admin(message: types.Message):
    event_name = EVENTS.get('sent_to_admin')
    user_properties = {'user_id': message.from_user.i}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def no_tries(message: types.Message) -> None:
    event_name = EVENTS.get('no_tries')
    user_properties = {'user_id': message.from_user.id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def invite_user(message: types.Message,
                      ref_user_id: int) -> None:
    event_name = EVENTS.get('invite')
    user_properties = {'user_id': message.from_user.id,
                       'ref_user_id': ref_user_id}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def send_estimate(message: types.Message,
                        text: str) -> None:
    event_name = 'User sent like/dislike'
    user_properties = {'user_id': message.from_user.id,
                       'mark': text}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def user_sub(message: types.Message,
                   text: str) -> None:
    event_name = 'User subscribed to the group'
    user_properties = {'user_id': message.from_user.id,
                       'group': text}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def user_sub_all(message: types.Message,
                       amount: int) -> None:
    event_name = 'User subscribed to all groups'
    user_properties = {'user_id': message.from_user.id,
                       'amount': amount}
    await send_and_log(event_name, message.from_user.id,
                       user_properties=user_properties)


async def response_from_runpod(user_id: int, ex_time: float) -> None:
    event_name = 'Got response from runpod'
    user_properties = {'execute time': ex_time,
                       'user_id': user_id}
    await send_and_log(event_name, user_properties=user_properties)


async def req_runpod(user_id: int) -> None:
    event_name = 'Sent request to runpod'
    user_properties = {'user_id': user_id}
    await send_and_log(event_name, user_properties=user_properties)

# coding=UTF-8
from threading import Thread
from gtts import gTTS
from vk_api import VkApi
from vk_api import bot_longpoll
from vk_api import VkUpload
from vk_api import utils
import os

token = ""
group = 1
vk_session = VkApi(token=token)
vk = vk_session.get_api()
longpool = bot_longpoll.VkBotLongPoll(vk=vk_session, group_id=group)


def tts(peer_id, mid, text):
    id = peer_id + mid
    gTTS(text=text, lang="ru").save(str(id) + ".mp3")
    audio = VkUpload(vk_session).audio_message(audio=str(id) + ".mp3", peer_id=peer_id)
    owner = audio['audio_message']['owner_id']
    audio_id = audio['audio_message']['id']
    vk.messages.send(
        message="vk.com/doc" + str(owner) + "_" + str(audio_id),
        random_id=utils.get_random_id(),
        peer_id=peer_id,
        reply_to=mid,
        attachment="doc" + str(owner) + "_" + str(audio_id)
    )
    os.remove(str(id) + ".mp3")
    print("Озвучил сообщение от " + str(peer_id) + ": " + text)


for event in longpool.listen():
    peer_id = event.message.peer_id
    text = event.message.text.lower()
    mid = event.message.id
    vk.messages.send(
        message="Ваше сообщение поставленно в очередь на озвучивание, ожидайте",
        random_id=utils.get_random_id(),
        peer_id=peer_id
    )
    Thread(target=tts, args=(peer_id, mid, text)).start()
    print("Поставил в очередь сообщение от " + str(peer_id) + ": " + text)

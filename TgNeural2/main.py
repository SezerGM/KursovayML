import telebot
import traceback
from handler import *
from keras.models import load_model
from PIL import Image, ImageOps
import tensorflow as tf
import io

token = '6984603153:AAHWrGB3v99PHxBswRNOON_XQ_tREgoq4ho'
bot = telebot.TeleBot(token)
classes = ['0', '9', '8', '7', '6', '5', '4', '3','2','1']
model = load_model('model.h5')

def get_photo(message):
    photo = message.photo[1].file_id
    file_info = bot.get_file(photo)
    file_content = bot.download_file(file_info.file_path)
    return file_content

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Send photo for classification")

@bot.message_handler(content_types=['photo'])
@bot.message_handler(content_types=['photo'])
def repeat_all_messages(message):
    try:
        file_content = get_photo(message)
        image = Image.open(io.BytesIO(file_content))
        image = image.convert('L')  # Convert to grayscale
        image = image.resize((28, 28))
        img_array = tf.keras.utils.img_to_array(image)
        img_array = tf.expand_dims(img_array, 0)

        # Ensure the input shape matches the model's expectations
        img_array = img_array[:, :, :, 0:1]

        predictions = model.predict(img_array)
        max_index = np.argmax(predictions)
        bot.send_message(message.chat.id, text=f'The probable classification for this photo is {classes[max_index]}')

    except Exception as e:
        traceback.print_exc()
        bot.send_message(message.chat.id, 'Something went wrong')


if __name__ == '__main__':
    import time

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(15)
            print('Restart!')
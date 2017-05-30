import ujson
from copy import deepcopy
from flask_sqlalchemy import sqlalchemy
from telegram import (
    ParseMode, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
)

from ... import db
from ...models import (
    Sentence, Paraphrase, SentenceBinary, SentenceSimilairty,
    TelegramUser
)
from .botfsm import BotGraphMachine
from .botfsm.mixins import TelegramBotUpdateConditionMixin




class LabelingMachine(BotGraphMachine, TelegramBotUpdateConditionMixin):
    # Conditions
    def is_asking_usage(self, event):
        text = event.message.text
        return text in ('/help', '/usage', '/start')

    def is_asking_for_alternavtive_q(self, event):
        text = event.message.text
        return '1' in text

    def is_asking_for_binary_q(self, event):
        text = event.message.text
        return '2' in text

    def is_asking_for_similarity_q(self, event):
        text = event.message.text
        return '3' in text

    def is_answering_binary_q(self, event):
        callback_data = ujson.loads(event.callback_query.data)
        return callback_data['type'] == 'binary'

    def is_answering_similarity_q(self, event):
        callback_data = ujson.loads(event.callback_query.data)
        return callback_data['type'] == 'similarity'

    def is_answering(self, event):
        text = event.message.text
        return text != 'quit'

    def is_quitting(self, event):
        text = event.message.text
        return text in ('/quit')

    # Helper Functions
    @staticmethod
    def get_or_create_telegramuser(from_user):
        user_id = from_user.id
        telegram_user = TelegramUser.query.filter_by(
            id=user_id
        ).first()
        if not telegram_user:
            telegram_user = TelegramUser(
                **from_user.to_dict()
            )
            db.session.add(telegram_user)
            db.session.commit()

        return telegram_user

    @staticmethod
    def get_message_or_calbcak_query_message(event):
        if event.message:
            return event.message
        elif event.callback_query.message:
            return event.callback_query.message


    def send_thank_you_message(self, event):
        message = self.get_message_or_calbcak_query_message(event)
        message.reply_text(
            text=self.render_text('thanks.j2')
        )

    # Operations
    def on_enter_ask_usage(self, event):
        event.message.reply_text(
            self.render_text('usage.j2')
        )
        self.bot_finish_ans()

    def on_enter_wait_user_alternative(self, event):
        telegram_user = self.get_or_create_telegramuser(event.message.from_user)

        sentence = Sentence.query.order_by(sqlalchemy.func.random()).first()
        paraphrase = Paraphrase(
            content='',
            sentence_id=sentence.id,
            created_by=telegram_user.id
        )
        db.session.add(paraphrase)
        db.session.commit()

        event.message.reply_text(
            self.render_text(
                'ask_alternative.j2',
                {'sentence': sentence}
            )
        )

    def on_enter_receive_user_alternative(self, event):
        if self.is_answering(event):
            user_id = event.message.from_user.id
            telegram_user = TelegramUser.query.filter_by(id=user_id).first()
            paraphrase = (
                Paraphrase.query
                          .filter_by(created_by=telegram_user.id)
                          .order_by(Paraphrase.created_at.desc())
                          .first()
            )
            paraphrase.content = event.message.text
            db.session.add(paraphrase)
            db.session.commit()

            self.continue_answering(event)
        else:
            self.quit_answering(event)

    def on_enter_wait_user_binary_response(self, event):
        sentence = Sentence.query.order_by(sqlalchemy.func.random()).first()
        paraphrase = Paraphrase.query.order_by(sqlalchemy.func.random()).first()

        def create_callback_button(ans):
            return ujson.dumps(
                {
                    'type': 'binary',
                    'sid': sentence.id,
                    'pid': paraphrase.id,
                    'ans': ans,
                }
            )

        is_similar_keyboard = [
            [InlineKeyboardButton(text='Yes', callback_data=create_callback_button(True)),
             InlineKeyboardButton(text='No', callback_data=create_callback_button(False))]
        ]
        reply_markup = InlineKeyboardMarkup(is_similar_keyboard)

        message = self.get_message_or_calbcak_query_message(event)
        message.reply_text(
            self.render_text(
                'ask_binary.j2',
                {
                    'sentence': sentence,
                    'paraphrase': paraphrase
                }
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        self.send_thank_you_message(event)
        self.bot_finish_ans()

    def on_enter_receive_user_binary_response(self, event):
        callback_data = ujson.loads(event.callback_query.data)

        telegram_user = self.get_or_create_telegramuser(event.callback_query.from_user)

        sentence_binary = SentenceBinary(
            paraphrase_id=callback_data['pid'],
            sentence_id=callback_data['sid'],
            is_similar=callback_data['ans'],
            created_by=telegram_user.id
        )
        db.session.add(sentence_binary)
        db.session.commit()

        self.send_thank_you_message(event)
        self.continue_answering(event)

    def on_enter_wait_user_similarity_score(self, event):
        sentence = Sentence.query.order_by(sqlalchemy.func.random()).first()
        paraphrase = Paraphrase.query.order_by(sqlalchemy.func.random()).first()

        def create_callback_button(ans):
            return ujson.dumps(
                {
                    'type': 'similarity',
                    'sid': sentence.id,
                    'pid': paraphrase.id,
                    'ans': ans,
                }
            )

        similarity_keyboard = [
            [InlineKeyboardButton(text=str(num), callback_data=create_callback_button(num))
             for num in range(1, 6)]
        ]
        reply_markup = InlineKeyboardMarkup(similarity_keyboard)

        message = self.get_message_or_calbcak_query_message(event)
        message.reply_text(
            self.render_text(
                'ask_similarity.j2',
                {
                    'sentence': sentence,
                    'paraphrase': paraphrase
                }
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )
        self.bot_finish_ans()

    def on_enter_receive_user_similarity_score(self, event):
        callback_data = ujson.loads(event.callback_query.data)

        telegram_user = self.get_or_create_telegramuser(event.callback_query.from_user)

        sentence_similarity = SentenceSimilairty(
            paraphrase_id=callback_data['pid'],
            sentence_id=callback_data['sid'],
            score=callback_data['ans'],
            created_by=telegram_user.id
        )
        db.session.add(sentence_similarity)
        db.session.commit()

        self.send_thank_you_message(event)
        self.continue_answering(event)

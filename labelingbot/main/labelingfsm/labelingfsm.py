from flask_sqlalchemy import sqlalchemy
from telegram import ParseMode

from ... import db
from ...models import (
    Sentence, Paraphrase, SentenceBinary, SentenceSimilairty,
    TelegramUser
)
from .botfsm import BotGraphMachine


class LabelingMachine(BotGraphMachine):
    # Conditions
    def is_asking_usage(self, event):
        text = event.message.text
        return 'help' in text

    def is_answering_alternative(self, event):
        text = event.message.text
        return '1' in text

    def is_answering_binary(self, event):
        text = event.message.text
        return '2' in text

    def is_answering_score(self, event):
        text = event.message.text
        return '3' in text

    def is_answering(self, event):
        text = event.message.text
        return text != 'quit'

    def is_quitting(self, event):
        text = event.message.text
        return text == 'quit'

    # Helper Functions
    @staticmethod
    def get_or_create_telegramuser(event):
        chat_id = event.message.chat_id
        telegram_user = TelegramUser.query.filter_by(
            id=chat_id
        ).first()
        if not telegram_user:
            telegram_user = TelegramUser(
                **event.message.from_user.to_dict()
            )
            db.session.add(telegram_user)
            db.session.commit()

        return telegram_user

    # Operations
    def on_enter_ask_usage(self, event):
        event.message.reply_text(
            self.render_text('usage.j2')
        )
        self.bot_finish_ans()

    def on_enter_wait_user_alternative(self, event):
        telegram_user = self.get_or_create_telegramuser(event)

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
            chat_id = event.message.chat_id
            telegram_user = TelegramUser.query.filter_by(id=chat_id).first()
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
        telegram_user = self.get_or_create_telegramuser(event)

        sentence = Sentence.query.order_by(sqlalchemy.func.random()).first()
        paraphrase = Paraphrase.query.order_by(sqlalchemy.func.random()).first()

        sentence_binary = SentenceBinary(
            paraphrase_id=paraphrase.id,
            sentence_id=sentence.id,
            created_by=telegram_user.id
        )
        db.session.add(sentence_binary)
        db.session.commit()

        event.message.reply_text(
            self.render_text(
                'ask_binary.j2',
                {
                    'sentence': sentence,
                    'paraphrase': paraphrase
                }
            ),
            parse_mode=ParseMode.MARKDOWN
        )

    def on_enter_receive_user_binary_response(self, event):
        if self.is_answering(event):
            chat_id = event.message.chat_id
            telegram_user = TelegramUser.query.filter_by(id=chat_id).first()
            sentence_binary = (
                SentenceBinary.query
                              .filter_by(created_by=telegram_user.id)
                              .order_by(SentenceBinary.created_at.desc())
                              .first()
            )
            sentence_binary.is_similar = (event.message.text == 'y')
            db.session.add(sentence_binary)
            db.session.commit()

            self.continue_answering(event)
        else:
            self.quit_answering(event)

    def on_enter_wait_user_similarity_score(self, event):
        telegram_user = self.get_or_create_telegramuser(event)

        sentence = Sentence.query.order_by(sqlalchemy.func.random()).first()
        paraphrase = Paraphrase.query.order_by(sqlalchemy.func.random()).first()

        sentence_similarity = SentenceSimilairty(
            paraphrase_id=paraphrase.id,
            sentence_id=sentence.id,
            created_by=telegram_user.id
        )
        db.session.add(sentence_similarity)
        db.session.commit()

        event.message.reply_text(
            self.render_text(
                'ask_similarity.j2',
                {
                    'sentence': sentence,
                    'paraphrase': paraphrase
                }
            )
        )

    def on_enter_receive_user_similarity_score(self, event):
        if self.is_answering(event):
            chat_id = event.message.chat_id
            telegram_user = TelegramUser.query.filter_by(id=chat_id).first()
            sentence_similarity = (
                SentenceSimilairty.query
                                  .filter_by(created_by=telegram_user.id)
                                  .order_by(SentenceSimilairty.created_at.desc())
                                  .first()
            )
            print(sentence_similarity.id)
            sentence_similarity.score = int(event.message.text)
            db.session.add(sentence_similarity)
            print(sentence_similarity.id)
            self.continue_answering(event)
        else:
            self.quit_answering(event)

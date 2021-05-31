# Generated by Django 3.2.2 on 2021-05-30 19:30

from django.db import migrations, models
import django.utils.timezone
import json.encoder
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(max_length=50, verbose_name='внешний идентификатор')),
                ('user_id', models.UUIDField(verbose_name='пользователь')),
                ('payment_system', models.CharField(max_length=50, verbose_name='платежная система')),
                ('type', models.CharField(max_length=50, verbose_name='тип')),
                ('is_default', models.BooleanField(default=False, verbose_name='по умолчанию')),
                ('data', models.JSONField(blank=True, decoder=json.decoder.JSONDecoder, default=dict, encoder=json.encoder.JSONEncoder, null=True, verbose_name='информация для фронта')),
            ],
            options={
                'verbose_name': 'метод оплаты',
                'verbose_name_plural': 'методы оплаты',
                'db_table': 'data"."payment_methods',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, verbose_name='название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='описание')),
                ('role_id', models.UUIDField(verbose_name='роль')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('period', models.IntegerField(verbose_name='период')),
                ('active', models.BooleanField(default=False, verbose_name='активен')),
                ('currency_code', models.CharField(max_length=3, verbose_name='код валюты')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'db_table': 'data"."products',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField(verbose_name='пользователь')),
                ('start_date', models.DateField(verbose_name='дата начала')),
                ('end_date', models.DateField(verbose_name='дата окончания')),
                ('state', models.CharField(choices=[('active', 'Активна'), ('pre_active', 'Оплачена'), ('to_deactivate', 'Готовится к отключению'), ('inactive', 'Неактивна'), ('cancelled', 'Отменена пользователем')], default='inactive', max_length=20, verbose_name='статус')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='subscription_product', to='billing.product', verbose_name='продукт')),
            ],
            options={
                'verbose_name': 'подписка',
                'verbose_name_plural': 'подписки',
                'db_table': 'data"."subscriptions',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', model_utils.fields.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('external_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='внешний идентификатор')),
                ('user_id', models.UUIDField(verbose_name='пользователь')),
                ('user_email', models.CharField(max_length=35)),
                ('state', models.CharField(choices=[('draft', 'Черновик'), ('processing', 'В процессе'), ('paid', 'Оплачен'), ('error', 'Ошибка')], default='draft', max_length=20, verbose_name='статус')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')),
                ('payment_currency_code', models.CharField(max_length=3, verbose_name='код валюты')),
                ('payment_system', models.CharField(max_length=50, verbose_name='платежная система')),
                ('is_automatic', models.BooleanField(default=False, verbose_name='автоматический')),
                ('is_refund', models.BooleanField(default=False, verbose_name='возврат')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_payment_method', to='billing.paymentmethod', verbose_name='способ оплаты')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_product', to='billing.product', verbose_name='продукт')),
                ('src_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='order_to_order', to='billing.order', verbose_name='оригинальный заказ')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_product', to='billing.subscription', verbose_name='подписка')),
            ],
            options={
                'verbose_name': 'заказ',
                'verbose_name_plural': 'заказы',
                'db_table': 'data"."orders',
            },
        ),
    ]

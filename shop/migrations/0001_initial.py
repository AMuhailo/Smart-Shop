# Generated by Django 5.2.3 on 2025-06-22 18:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
            ],
            options={
                'ordering': ['-title', '-id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_category', to='shop.category')),
            ],
            options={
                'ordering': ['-id'],
                'indexes': [models.Index(fields=['-id'], name='shop_produc_id_fb1096_idx'), models.Index(fields=['slug'], name='shop_produc_slug_76971b_idx'), models.Index(fields=['-price'], name='shop_produc_price_eee6c9_idx'), models.Index(fields=['-created'], name='shop_produc_created_ef211c_idx')],
            },
        ),
    ]

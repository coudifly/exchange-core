# Generated by Django 2.0.1 on 2018-07-13 16:39

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_core', '0001_squashed_0047_auto_20180706_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAccounts',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('deposit', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Deposit')),
                ('reserved', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Reserved')),
                ('deposit_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Deposit address')),
                ('address_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Address ID')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('currency', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='exchange_core.Currencies')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Currency account',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalBankAccounts',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('bank', models.CharField(choices=[('1', '1 - Banco do Brasil S.A.'), ('3', '3 - Banco da Amazônia S.A.'), ('4', '4 - Banco do Nordeste do Brasil S.A.'), ('12', '12 - Banco Standard de Investimentos S.A.'), ('14', '14 - Natixis Brasil S.A. Banco Múltiplo'), ('18', '18 - Banco Tricury S.A.'), ('19', '19 - Banco Azteca do Brasil S.A.'), ('21', '21 - BANESTES S.A. Banco do Estado do Espírito Santo'), ('24', '24 - Banco BANDEPE S.A.'), ('25', '25 - Banco Alfa S.A.'), ('29', '29 - Banco Banerj S.A.'), ('31', '31 - Banco Beg S.A.'), ('33', '33 - Banco Santander (Brasil) S.A.'), ('36', '36 - Banco Bradesco BBI S.A.'), ('37', '37 - Banco do Estado do Pará S.A.'), ('39', '39 - Banco do Estado do Piauí S.A. - BEP'), ('40', '40 - Banco Cargill S.A.'), ('41', '41 - Banco do Estado do Rio Grande do Sul S.A.'), ('44', '44 - Banco BVA S.A.'), ('45', '45 - Banco Opportunity S.A.'), ('47', '47 - Banco do Estado de Sergipe S.A.'), ('62', '62 - Hipercard Banco Múltiplo S.A.'), ('63', '63 - Banco Ibi S.A. Banco Múltiplo'), ('64', '64 - Goldman Sachs do Brasil Banco Múltiplo S.A.'), ('65', '65 - Banco AndBank (Brasil) S.A.'), ('66', '66 - Banco Morgan Stanley S.A.'), ('69', '69 - BPN Brasil Banco Múltiplo S.A.'), ('70', '70 - BRB - Banco de Brasília S.A.'), ('72', '72 - Banco Rural Mais S.A.'), ('73', '73 - BB Banco Popular do Brasil S.A.'), ('74', '74 - Banco J. Safra S.A.'), ('75', '75 - Banco ABN AMRO S.A.'), ('76', '76 - Banco KDB S.A.'), ('77', '77 - Banco Intermedium S.A.'), ('78', '78 - BES Investimento do Brasil S.A.-Banco de Investimento'), ('79', '79 - Banco Original do Agronegócio S.A.'), ('81', '81 - BBN Banco Brasileiro de Negócios S.A.'), ('82', '82 - Banco Topázio S.A.'), ('83', '83 - Banco da China Brasil S.A.'), ('85', '85 - Cooperativa Central de Crédito Urbano-CECRED'), ('86', '86 - OBOE Crédito Financiamento e Investimento S.A.'), ('87', '87 - Cooperativa Unicred Central Santa Catarina'), ('88', '88 - Banco Randon S.A.'), ('89', '89 - Cooperativa de Crédito Rural da Região de Mogiana'), ('90', '90 - Cooperativa Central de Economia e Crédito Mutuo das Unicreds'), ('91', '91 - Unicred Central do Rio Grande do Sul'), ('92', '92 - Brickell S.A. Crédito, financiamento e Investimento'), ('94', '94 - Banco Petra S.A.'), ('95', '95 - Banco Confidence de Câmbio S.A.'), ('96', '96 - Banco BM&FBOVESPA de Serviços de Liquidação e Custódia S.A'), ('97', '97 - Cooperativa Central de Crédito Noroeste Brasileiro Ltda.'), ('98', '98 - CREDIALIANÇA COOPERATIVA DE CRÉDITO RURAL'), ('99', '99 - Cooperativa Central de Economia e Credito Mutuo das Unicreds'), ('104', '104 - Caixa Econômica Federal'), ('107', '107 - Banco BBM S.A.'), ('114', '114 - Central das Coop. de Economia e Crédito Mutuo do Est. do ES'), ('119', '119 - Banco Western Union do Brasil S.A.'), ('122', '122 - Banco BERJ S.A.'), ('125', '125 - Brasil Plural S.A. - Banco Múltiplo'), ('136', '136 - CONFEDERACAO NACIONAL DAS COOPERATIVAS CENTRAIS UNICREDS'), ('168', '168 - HSBC Finance (Brasil) S.A. - Banco Múltiplo'), ('184', '184 - Banco Itaú BBA S.A.'), ('204', '204 - Banco Bradesco Cartões S.A.'), ('208', '208 - Banco BTG Pactual S.A.'), ('212', '212 - Banco Original S.A.'), ('213', '213 - Banco Arbi S.A.'), ('214', '214 - Banco Dibens S.A.'), ('215', '215 - Banco Comercial e de Investimento Sudameris S.A.'), ('217', '217 - Banco John Deere S.A.'), ('218', '218 - Banco Bonsucesso S.A.'), ('222', '222 - Banco Credit Agricole Brasil S.A.'), ('224', '224 - Banco Fibra S.A.'), ('225', '225 - Banco Brascan S.A.'), ('229', '229 - Banco Cruzeiro do Sul S.A.'), ('230', '230 - Unicard Banco Múltiplo S.A.'), ('233', '233 - Banco Cifra S.A.'), ('237', '237 - Banco Bradesco S.A.'), ('241', '241 - Banco Clássico S.A.'), ('243', '243 - Banco Máxima S.A.'), ('246', '246 - Banco ABC Brasil S.A.'), ('248', '248 - Banco Boavista Interatlântico S.A.'), ('249', '249 - Banco Investcred Unibanco S.A.'), ('250', '250 - BCV - Banco de Crédito e Varejo S.A.'), ('254', '254 - Paraná Banco S.A.'), ('263', '263 - Banco Cacique S.A.'), ('265', '265 - Banco Fator S.A.'), ('266', '266 - Banco Cédula S.A.'), ('300', '300 - Banco de La Nacion Argentina'), ('318', '318 - Banco BMG S.A.'), ('320', '320 - Banco Industrial e Comercial S.A.'), ('341', '341 - Itaú Unibanco S.A.'), ('356', '356 - Banco Real S.A.'), ('366', '366 - Banco Société Générale Brasil S.A.'), ('370', '370 - Banco Mizuho do Brasil S.A.'), ('376', '376 - Banco J. P. Morgan S.A.'), ('389', '389 - Banco Mercantil do Brasil S.A.'), ('394', '394 - Banco Bradesco Financiamentos S.A.'), ('399', '399 - HSBC Bank Brasil S.A. - Banco Múltiplo'), ('409', '409 - UNIBANCO - União de Bancos Brasileiros S.A.'), ('412', '412 - Banco Capital S.A.'), ('422', '422 - Banco Safra S.A.'), ('453', '453 - Banco Rural S.A.'), ('456', '456 - Banco de Tokyo-Mitsubishi UFJ Brasil S.A.'), ('464', '464 - Banco Sumitomo Mitsui Brasileiro S.A.'), ('473', '473 - Banco Caixa Geral - Brasil S.A.'), ('477', '477 - CitiBank S.A.'), ('479', '479 - Banco ItaúBank S.A'), ('487', '487 - Deutsche Bank S.A. - Banco Alemão'), ('488', '488 - JPMorgan Chase Bank'), ('492', '492 - ING Bank N.V.'), ('494', '494 - Banco de La Republica Oriental del Uruguay'), ('495', '495 - Banco de La Provincia de Buenos Aires'), ('505', '505 - Banco Credit Suisse (Brasil) S.A.'), ('600', '600 - Banco Luso Brasileiro S.A.'), ('604', '604 - Banco Industrial do Brasil S.A.'), ('610', '610 - Banco VR S.A.'), ('611', '611 - Banco Paulista S.A.'), ('612', '612 - Banco Guanabara S.A.'), ('613', '613 - Banco Pecúnia S.A.'), ('623', '623 - Banco PAN S.A.'), ('626', '626 - Banco Ficsa S.A.'), ('630', '630 - Banco Intercap S.A.'), ('633', '633 - Banco Rendimento S.A.'), ('634', '634 - Banco Triângulo S.A.'), ('637', '637 - Banco Sofisa S.A.'), ('638', '638 - Banco Prosper S.A.'), ('641', '641 - Banco Alvorada S.A.'), ('643', '643 - Banco Pine S.A.'), ('652', '652 - Itaú Unibanco Holding S.A.'), ('653', '653 - Banco Indusval S.A.'), ('654', '654 - Banco A.J.Renner S.A.'), ('655', '655 - Banco Votorantim S.A.'), ('707', '707 - Banco Daycoval S.A.'), ('712', '712 - Banco Ourinvest S.A.'), ('719', '719 - Banif-Banco Internacional do Funchal (Brasil)S.A.'), ('721', '721 - Banco Credibel S.A.'), ('724', '724 - Banco Porto Seguro S.A.'), ('734', '734 - Banco Gerdau S.A.'), ('735', '735 - Banco Pottencial S.A.'), ('738', '738 - Banco Morada S.A.'), ('739', '739 - Banco Cetelem S.A.'), ('740', '740 - Banco Barclays S.A.'), ('741', '741 - Banco Ribeirão Preto S.A.'), ('743', '743 - Banco Semear S.A.'), ('744', '744 - BankBoston N.A.'), ('745', '745 - Banco CitiBank S.A.'), ('746', '746 - Banco Modal S.A.'), ('747', '747 - Banco RaboBank International Brasil S.A.'), ('748', '748 - Banco Cooperativo Sicredi S.A.'), ('749', '749 - Banco Simples S.A.'), ('751', '751 - ScotiaBank Brasil S.A. Banco Múltiplo'), ('752', '752 - Banco BNP Paribas Brasil S.A.'), ('753', '753 - NBC Bank Brasil S.A. - Banco Múltiplo'), ('755', '755 - Bank of America Merrill Lynch Banco Múltiplo S.A.'), ('756', '756 - Banco Cooperativo do Brasil S.A. - BANCOOB'), ('757', '757 - Banco KEB do Brasil S.A.')], max_length=10, verbose_name='Bank')),
                ('agency', models.CharField(max_length=10, verbose_name='Agency')),
                ('agency_digit', models.CharField(max_length=5, null=True, verbose_name='Digit')),
                ('account_type', models.CharField(choices=[('corrente', 'Corrente'), ('poupanca', 'Poupança')], max_length=20, verbose_name='Account type')),
                ('account_number', models.CharField(max_length=20, verbose_name='Account number')),
                ('account_number_digit', models.CharField(max_length=5, null=True, verbose_name='Digit')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('account', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='exchange_core.Accounts')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Bank account',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalBankWithdraw',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('deposit', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Deposit')),
                ('reserved', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Reserved')),
                ('amount', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Amount')),
                ('fee', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Fee')),
                ('status', models.CharField(choices=[('requested', 'requested'), ('reversed', 'reversed'), ('paid', 'paid')], default='requested', max_length=20, verbose_name='Status')),
                ('tx_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='Transaction id')),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Description')),
                ('bank', models.CharField(choices=[('1', '1 - Banco do Brasil S.A.'), ('3', '3 - Banco da Amazônia S.A.'), ('4', '4 - Banco do Nordeste do Brasil S.A.'), ('12', '12 - Banco Standard de Investimentos S.A.'), ('14', '14 - Natixis Brasil S.A. Banco Múltiplo'), ('18', '18 - Banco Tricury S.A.'), ('19', '19 - Banco Azteca do Brasil S.A.'), ('21', '21 - BANESTES S.A. Banco do Estado do Espírito Santo'), ('24', '24 - Banco BANDEPE S.A.'), ('25', '25 - Banco Alfa S.A.'), ('29', '29 - Banco Banerj S.A.'), ('31', '31 - Banco Beg S.A.'), ('33', '33 - Banco Santander (Brasil) S.A.'), ('36', '36 - Banco Bradesco BBI S.A.'), ('37', '37 - Banco do Estado do Pará S.A.'), ('39', '39 - Banco do Estado do Piauí S.A. - BEP'), ('40', '40 - Banco Cargill S.A.'), ('41', '41 - Banco do Estado do Rio Grande do Sul S.A.'), ('44', '44 - Banco BVA S.A.'), ('45', '45 - Banco Opportunity S.A.'), ('47', '47 - Banco do Estado de Sergipe S.A.'), ('62', '62 - Hipercard Banco Múltiplo S.A.'), ('63', '63 - Banco Ibi S.A. Banco Múltiplo'), ('64', '64 - Goldman Sachs do Brasil Banco Múltiplo S.A.'), ('65', '65 - Banco AndBank (Brasil) S.A.'), ('66', '66 - Banco Morgan Stanley S.A.'), ('69', '69 - BPN Brasil Banco Múltiplo S.A.'), ('70', '70 - BRB - Banco de Brasília S.A.'), ('72', '72 - Banco Rural Mais S.A.'), ('73', '73 - BB Banco Popular do Brasil S.A.'), ('74', '74 - Banco J. Safra S.A.'), ('75', '75 - Banco ABN AMRO S.A.'), ('76', '76 - Banco KDB S.A.'), ('77', '77 - Banco Intermedium S.A.'), ('78', '78 - BES Investimento do Brasil S.A.-Banco de Investimento'), ('79', '79 - Banco Original do Agronegócio S.A.'), ('81', '81 - BBN Banco Brasileiro de Negócios S.A.'), ('82', '82 - Banco Topázio S.A.'), ('83', '83 - Banco da China Brasil S.A.'), ('85', '85 - Cooperativa Central de Crédito Urbano-CECRED'), ('86', '86 - OBOE Crédito Financiamento e Investimento S.A.'), ('87', '87 - Cooperativa Unicred Central Santa Catarina'), ('88', '88 - Banco Randon S.A.'), ('89', '89 - Cooperativa de Crédito Rural da Região de Mogiana'), ('90', '90 - Cooperativa Central de Economia e Crédito Mutuo das Unicreds'), ('91', '91 - Unicred Central do Rio Grande do Sul'), ('92', '92 - Brickell S.A. Crédito, financiamento e Investimento'), ('94', '94 - Banco Petra S.A.'), ('95', '95 - Banco Confidence de Câmbio S.A.'), ('96', '96 - Banco BM&FBOVESPA de Serviços de Liquidação e Custódia S.A'), ('97', '97 - Cooperativa Central de Crédito Noroeste Brasileiro Ltda.'), ('98', '98 - CREDIALIANÇA COOPERATIVA DE CRÉDITO RURAL'), ('99', '99 - Cooperativa Central de Economia e Credito Mutuo das Unicreds'), ('104', '104 - Caixa Econômica Federal'), ('107', '107 - Banco BBM S.A.'), ('114', '114 - Central das Coop. de Economia e Crédito Mutuo do Est. do ES'), ('119', '119 - Banco Western Union do Brasil S.A.'), ('122', '122 - Banco BERJ S.A.'), ('125', '125 - Brasil Plural S.A. - Banco Múltiplo'), ('136', '136 - CONFEDERACAO NACIONAL DAS COOPERATIVAS CENTRAIS UNICREDS'), ('168', '168 - HSBC Finance (Brasil) S.A. - Banco Múltiplo'), ('184', '184 - Banco Itaú BBA S.A.'), ('204', '204 - Banco Bradesco Cartões S.A.'), ('208', '208 - Banco BTG Pactual S.A.'), ('212', '212 - Banco Original S.A.'), ('213', '213 - Banco Arbi S.A.'), ('214', '214 - Banco Dibens S.A.'), ('215', '215 - Banco Comercial e de Investimento Sudameris S.A.'), ('217', '217 - Banco John Deere S.A.'), ('218', '218 - Banco Bonsucesso S.A.'), ('222', '222 - Banco Credit Agricole Brasil S.A.'), ('224', '224 - Banco Fibra S.A.'), ('225', '225 - Banco Brascan S.A.'), ('229', '229 - Banco Cruzeiro do Sul S.A.'), ('230', '230 - Unicard Banco Múltiplo S.A.'), ('233', '233 - Banco Cifra S.A.'), ('237', '237 - Banco Bradesco S.A.'), ('241', '241 - Banco Clássico S.A.'), ('243', '243 - Banco Máxima S.A.'), ('246', '246 - Banco ABC Brasil S.A.'), ('248', '248 - Banco Boavista Interatlântico S.A.'), ('249', '249 - Banco Investcred Unibanco S.A.'), ('250', '250 - BCV - Banco de Crédito e Varejo S.A.'), ('254', '254 - Paraná Banco S.A.'), ('263', '263 - Banco Cacique S.A.'), ('265', '265 - Banco Fator S.A.'), ('266', '266 - Banco Cédula S.A.'), ('300', '300 - Banco de La Nacion Argentina'), ('318', '318 - Banco BMG S.A.'), ('320', '320 - Banco Industrial e Comercial S.A.'), ('341', '341 - Itaú Unibanco S.A.'), ('356', '356 - Banco Real S.A.'), ('366', '366 - Banco Société Générale Brasil S.A.'), ('370', '370 - Banco Mizuho do Brasil S.A.'), ('376', '376 - Banco J. P. Morgan S.A.'), ('389', '389 - Banco Mercantil do Brasil S.A.'), ('394', '394 - Banco Bradesco Financiamentos S.A.'), ('399', '399 - HSBC Bank Brasil S.A. - Banco Múltiplo'), ('409', '409 - UNIBANCO - União de Bancos Brasileiros S.A.'), ('412', '412 - Banco Capital S.A.'), ('422', '422 - Banco Safra S.A.'), ('453', '453 - Banco Rural S.A.'), ('456', '456 - Banco de Tokyo-Mitsubishi UFJ Brasil S.A.'), ('464', '464 - Banco Sumitomo Mitsui Brasileiro S.A.'), ('473', '473 - Banco Caixa Geral - Brasil S.A.'), ('477', '477 - CitiBank S.A.'), ('479', '479 - Banco ItaúBank S.A'), ('487', '487 - Deutsche Bank S.A. - Banco Alemão'), ('488', '488 - JPMorgan Chase Bank'), ('492', '492 - ING Bank N.V.'), ('494', '494 - Banco de La Republica Oriental del Uruguay'), ('495', '495 - Banco de La Provincia de Buenos Aires'), ('505', '505 - Banco Credit Suisse (Brasil) S.A.'), ('600', '600 - Banco Luso Brasileiro S.A.'), ('604', '604 - Banco Industrial do Brasil S.A.'), ('610', '610 - Banco VR S.A.'), ('611', '611 - Banco Paulista S.A.'), ('612', '612 - Banco Guanabara S.A.'), ('613', '613 - Banco Pecúnia S.A.'), ('623', '623 - Banco PAN S.A.'), ('626', '626 - Banco Ficsa S.A.'), ('630', '630 - Banco Intercap S.A.'), ('633', '633 - Banco Rendimento S.A.'), ('634', '634 - Banco Triângulo S.A.'), ('637', '637 - Banco Sofisa S.A.'), ('638', '638 - Banco Prosper S.A.'), ('641', '641 - Banco Alvorada S.A.'), ('643', '643 - Banco Pine S.A.'), ('652', '652 - Itaú Unibanco Holding S.A.'), ('653', '653 - Banco Indusval S.A.'), ('654', '654 - Banco A.J.Renner S.A.'), ('655', '655 - Banco Votorantim S.A.'), ('707', '707 - Banco Daycoval S.A.'), ('712', '712 - Banco Ourinvest S.A.'), ('719', '719 - Banif-Banco Internacional do Funchal (Brasil)S.A.'), ('721', '721 - Banco Credibel S.A.'), ('724', '724 - Banco Porto Seguro S.A.'), ('734', '734 - Banco Gerdau S.A.'), ('735', '735 - Banco Pottencial S.A.'), ('738', '738 - Banco Morada S.A.'), ('739', '739 - Banco Cetelem S.A.'), ('740', '740 - Banco Barclays S.A.'), ('741', '741 - Banco Ribeirão Preto S.A.'), ('743', '743 - Banco Semear S.A.'), ('744', '744 - BankBoston N.A.'), ('745', '745 - Banco CitiBank S.A.'), ('746', '746 - Banco Modal S.A.'), ('747', '747 - Banco RaboBank International Brasil S.A.'), ('748', '748 - Banco Cooperativo Sicredi S.A.'), ('749', '749 - Banco Simples S.A.'), ('751', '751 - ScotiaBank Brasil S.A. Banco Múltiplo'), ('752', '752 - Banco BNP Paribas Brasil S.A.'), ('753', '753 - NBC Bank Brasil S.A. - Banco Múltiplo'), ('755', '755 - Bank of America Merrill Lynch Banco Múltiplo S.A.'), ('756', '756 - Banco Cooperativo do Brasil S.A. - BANCOOB'), ('757', '757 - Banco KEB do Brasil S.A.')], max_length=10, verbose_name='Bank')),
                ('agency', models.CharField(max_length=10, verbose_name='Agency')),
                ('agency_digit', models.CharField(max_length=5, null=True, verbose_name='Digit')),
                ('account_type', models.CharField(choices=[('corrente', 'Corrente'), ('poupanca', 'Poupança')], max_length=20, verbose_name='Account type')),
                ('account_number', models.CharField(max_length=20, verbose_name='Account number')),
                ('account_number_digit', models.CharField(max_length=5, null=True, verbose_name='Digit')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('account', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='exchange_core.Accounts')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Bank withdraw',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCryptoWithdraw',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('code', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('deposit', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Deposit')),
                ('reserved', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Reserved')),
                ('amount', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Amount')),
                ('fee', models.DecimalField(decimal_places=8, default=Decimal('0.00'), max_digits=20, verbose_name='Fee')),
                ('status', models.CharField(choices=[('requested', 'requested'), ('reversed', 'reversed'), ('paid', 'paid')], default='requested', max_length=20, verbose_name='Status')),
                ('tx_id', models.CharField(blank=True, max_length=150, null=True, verbose_name='Transaction id')),
                ('description', models.CharField(max_length=100, null=True, verbose_name='Description')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('account', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='exchange_core.Accounts')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Crypto withdraw',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
        migrations.CreateModel(
            name='HistoricalCurrencies',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('symbol', models.CharField(max_length=10, verbose_name='Symbol')),
                ('type', models.CharField(choices=[('checking', 'checking'), ('investment', 'investment')], default='checking', max_length=20, verbose_name='Type')),
                ('icon', models.TextField(blank=True, max_length=100, null=True, verbose_name='Icon')),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=30, verbose_name='Status')),
                ('withdraw_min', models.DecimalField(decimal_places=8, default=Decimal('0.0'), max_digits=20, verbose_name='Withdraw Min')),
                ('withdraw_max', models.DecimalField(decimal_places=8, default=Decimal('1000000.00'), max_digits=20, verbose_name='Withdraw Max')),
                ('withdraw_fee', models.DecimalField(decimal_places=8, default=Decimal('0.0'), max_digits=20, verbose_name='Withdraw Percent Fee')),
                ('withdraw_fixed_fee', models.DecimalField(decimal_places=8, default=Decimal('0.0'), max_digits=20, verbose_name='Withdraw Fixed Fee')),
                ('tbsa_fee', models.DecimalField(decimal_places=8, default=Decimal('0.0'), help_text='Transfer between system accounts', max_digits=20, verbose_name='TBSA Percent Fee')),
                ('tbsa_fixed_fee', models.DecimalField(decimal_places=8, default=Decimal('0.0'), help_text='Transfer between system accounts', max_digits=20, verbose_name='TBSA Fixed Fee')),
                ('withdraw_receive_hours', models.IntegerField(default=48, verbose_name='Withdraw receive hours')),
                ('order', models.IntegerField(default=100, verbose_name='Order')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Currency',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
        ),
    ]

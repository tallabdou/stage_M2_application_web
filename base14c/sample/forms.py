from django.forms import ModelForm
from .models import Sample
from .fields import ListTextWidget


class SampleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        _country_list = kwargs.pop('data_list', None)
        super(SampleForm, self).__init__(*args, **kwargs)

        self.fields['sample_reference_blank'].widget = ListTextWidget(
            data_list=('sample',	'OXA 2',	'OXA 1',	'IAEA C1',	'IAEA C2',	'IAEA C7',	'IAEA C8',
                       'PHA',	'AfS',	'C 1-EDM',	'C 2-EDM',	'BLC corail',	'FIRI H',
                       'BLC stalagmite',	'Sclayn',	'AIEA-C 3',	'FIRI D',	'El Akarit',
                       'SIRI G',	'SIRI J',	'VIRI Q',	'FIRI A',	'SIRI E',	'FIRI C',
                       'VIRI I',	'VIRI F',	'VIRI E',	'Gerde 1',	'Chiloe CH/Ta',	'VIRI U',
                       'VIRI O',	'A2 Mammoth'), name='blank')

        self.fields['sample_type'].widget = ListTextWidget(
            data_list=('ac. Oxalique',	'ac. Phtalique', 'bois',	'boyau',	'carbonate',	'cellulose',
                       'charbon',	'CO2',	'collagène',	'colophane',	'coquillage',	'corail benth',
                       'dent',	'DIC',	'DOC lyoph',	'eau',	'foram benth',	'foram plk',	'forams n.d.',
                       'gasteropode',	'graines',	'granule de ver de terre',	'huile',	'humic acid',	'insect',
                       'macrorestes anim',	'macrorestes veg',	'marbre',	'MO',	'n.d.',	'organic',
                       'organic compound',	'os',	'parenchyme',	'peinture rupestre',	'POC filtre',
                       'pollen',	'racine',	'sédiment bulk',	'sol adhérent',	'sol bulk',	'sol nu',
                       'stalagmite',	'travertin',	'turbidite',	'vernis',	'laque',	'végétaux'), name='add_inf')

        self.fields['sample_fraction_analysed'].widget = ListTextWidget(
            data_list=('ac. Oxalique',	'ac. Phtalique',	'BaCO3',	'bois',	'carbonate',	'cellulose',	'charbon',
                       'charge (peinture)',	'CO2',	'collagène',	'colophane',	'DIC',	'huile',	'humic acid',
                       'MO',	'n.d.',	'organic compound',	'PbCO3',	'pigment (peinture)',	'POC filtre',	'perfect bulk',
                       'bulk after water rinsing (loss of aminoacid, sugar…)'),   name='fraction')

    class Meta:
        model = Sample
        fields = '__all__'

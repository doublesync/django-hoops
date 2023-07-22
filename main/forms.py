# Custom imports
import json

# Django imports
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

# Main imports
from .league import config as league_config
from copy import deepcopy

player_styles = open("main/league/looyh/styles.json")
player_styles = json.load(player_styles)

class PlayerForm(forms.Form):
    # Get attribute_choices
    attribute_choices_config = league_config.attribute_choices
    attribute_choices = []
    for tuple in attribute_choices_config:
        if not tuple[0] in league_config.attribute_categories["physical"]:
            attribute_choices.append(tuple)
    # Create fields
    first_name = forms.CharField(label="First Name", max_length=16)
    last_name = forms.CharField(label="Last Name", max_length=16)
    cyberface = forms.IntegerField(label="Cyberface", min_value=0, max_value=40000)
    height = forms.ChoiceField(label="Height", choices=league_config.height_choices)
    weight = forms.IntegerField(
        label="Weight",
        min_value=league_config.player_weight_min,
        max_value=league_config.player_weight_max,
    )
    primary_position = forms.ChoiceField(
        label="Primary Position", choices=league_config.position_choices
    )
    secondary_position = forms.ChoiceField(
        label="Secondary Position", choices=league_config.position_choices
    )
    jersey_number = forms.IntegerField(
        label="Jersey Number", min_value=0, max_value=league_config.max_attribute
    )
    primary_attributes = forms.MultipleChoiceField(
        label="Primary Attributes",
        choices=attribute_choices,
        widget=forms.SelectMultiple(),
    )
    secondary_attributes = forms.MultipleChoiceField(
        label="Primary Attributes",
        choices=attribute_choices,
        widget=forms.SelectMultiple(),
    )
    primary_badges = forms.MultipleChoiceField(
        label="Primary Badges",
        choices=league_config.badge_choices,
        widget=forms.SelectMultiple(),
    )
    secondary_badges = forms.MultipleChoiceField(
        label="Secondary Badges",
        choices=league_config.badge_choices,
        widget=forms.SelectMultiple(),
    )
    referral_code = forms.IntegerField(label="Referral Code", required=False)

class UpgradeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(UpgradeForm, self).__init__(*args, **kwargs)
        # For each key in attributes, create integerfield
        for key in league_config.initial_attributes:
            if key in league_config.attribute_categories["physical"]:
                continue
            self.fields[key] = forms.IntegerField(
                label=key,
                min_value=0,
                max_value=league_config.max_attribute,
                widget=forms.NumberInput(attrs={"onchange": "updatePrice()"}),
            )
        # For each key in badges, create choicefield
        for key in league_config.initial_badges:
            self.fields[key] = forms.ChoiceField(
                label=key,
                choices=league_config.badge_upgrade_choices,
                widget=forms.Select(attrs={"onchange": "updatePrice()"}),
            )
        # For each key in tendencies, create integerfield
        for key in league_config.initial_tendencies:
            # If players cannot change this tendency, skip
            if key in league_config.banned_tendencies:
                continue
            # If players can change this tendency, create field
            self.fields[key] = forms.IntegerField(
                label=key,
                min_value=league_config.min_tendency,
                max_value=league_config.max_tendency,
                widget=forms.NumberInput(attrs={"onchange": "updatePrice()"}),
            )
        # For each key in hotzones, create choicefield
        # for key in league_config.initial_hotzones:
        #     self.fields[key] = forms.ChoiceField(
        #         label=key,
        #         choices=league_config.hotzone_choices,
        #         widget=forms.Select(attrs={"onchange": "updatePrice()"}),
        #     )

class StylesForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(StylesForm, self).__init__(*args, **kwargs)
        for style, data in player_styles.items():
            # Create the ChoiceField
            self.fields[style] = forms.ChoiceField(
                label=style,
                choices=data["options"],
                widget=forms.Select(),
            )

class TradeForm(forms.Form):
    pass

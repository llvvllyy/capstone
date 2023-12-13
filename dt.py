from datetime import datetime
import pandas as pd
import os

class C45DecisionTree:
    def __init__(self, data):
        if isinstance(data, pd.DataFrame):
            self.df = data
        elif isinstance(data, str):  # Assume it's a file path
            csv_path = os.path.join(os.path.dirname(__file__), data)
            self.df = pd.read_csv(csv_path)
        else:
            raise ValueError("Input data should be a DataFrame or a CSV file path.")
    
    def convert_date(self, date_string):
        return datetime.strptime(date_string, '%Y-%m-%d')
    
    def determine_season(self, planting_date):
        if 6 <= planting_date.month <= 11:
            return 'Wet'
        else:
            return 'Dry'
    
    def calculate_days_to_maturity(self, planting_date, harvest_date):
        return (harvest_date - planting_date).days


    def predict_variety(self, type_, trait, domain, planting_date, target_harvest_date):
        # Convert dates to datetime objects
        planting_date = self.convert_date(planting_date)
        target_harvest_date = self.convert_date(target_harvest_date)

        # Determine season
        season = self.determine_season(planting_date)
        # print(f"The target date belongs to the {season} season.")

        # Initialize filtered_df with the entire dataset
        filtered_df = self.df.copy()

        # Priority 1: Filter based on Type
        if type_:
            filtered_df_type = filtered_df[filtered_df['type'] == type_]
            if not filtered_df_type.empty:
                filtered_df = filtered_df_type
            else:
                print(f"No valid variety for the selected type: {type_}.")
                return None, pd.DataFrame(columns=self.df.columns), 0  # Include the missing return value
        # print("Filtered based on Type:\n", filtered_df)

        # Priority 2: Filter based on Trait
        if trait:
            filtered_df_trait = filtered_df[filtered_df['trait'] == trait]
            if not filtered_df_trait.empty:
                filtered_df = filtered_df_trait
            else:
                print("No valid variety for the selected trait. Proceeding to the next priority.")
        # print("Filtered based on Trait:\n", filtered_df)

        # Priority 3: Filter based on Domain
        if domain:
            filtered_df_domain = filtered_df[filtered_df['domain'] == domain]
            if not filtered_df_domain.empty:
                filtered_df = filtered_df_domain
            else:
                print("No valid variety for the selected domain. Proceeding to the next priority.")
        # print("Filtered based on Domain:\n", filtered_df)

        # Priority 4: Filter based on Season
        # Continue with selecting a variety based on season if no match found
        season_column = f'maturity_ds' if season == 'Dry' else 'maturity_ws'

        # Handle empty cells in the selected season column
        while filtered_df[season_column].isnull().any():
            filtered_df = filtered_df[filtered_df[season_column].notnull()]
            # print(f"Filtered based on {season} season (excluding empty cells):\n{filtered_df}")

            # Calculate number of days
            days_to_maturity = self.calculate_days_to_maturity(planting_date, target_harvest_date)

            # Find the variety with the closest maturity
            if not filtered_df.empty and 'variety' in filtered_df.columns:
                selected_variety = filtered_df.loc[
                    abs(pd.to_numeric(filtered_df[season_column], errors='coerce') - days_to_maturity).idxmin(), 'variety'
                ]
                return selected_variety, filtered_df, days_to_maturity
            else:
                # If still no valid variety found, return None and an empty DataFrame
                # print("No valid variety for the selected features and season.")
                return None, pd.DataFrame(columns=self.df.columns), days_to_maturity

        # Calculate number of days
        days_to_maturity = self.calculate_days_to_maturity(planting_date, target_harvest_date)
        # print(f"Number of days to maturity: {days_to_maturity} days")

        # Find the variety with the closest maturity
        if not filtered_df.empty and 'variety' in filtered_df.columns:
            selected_variety = filtered_df.loc[
                abs(pd.to_numeric(filtered_df[season_column], errors='coerce') - days_to_maturity).idxmin(), 'variety'
            ]
            return selected_variety, filtered_df, days_to_maturity  # Include the missing return value

        # If still no valid variety found, return None and an empty DataFrame
        print("No valid variety for the selected features and season.")
        return None, pd.DataFrame(columns=self.df.columns), 0  # Include the missing return value

    def select_variety(self, filtered_df, days_to_maturity, season_column, planting_date, target_harvest_date, season):
        # Ensure that days_to_maturity is defined
        if days_to_maturity is None:
            days_to_maturity = self.calculate_days_to_maturity(planting_date, target_harvest_date)

        season_column = 'maturity_ds' if season == 'Dry' else 'maturity_ws'
        # print(f"Selected maturity column: {season_column}")
        
        # Initialize days_to_maturity to a default value
        days_to_maturity = days_to_maturity if days_to_maturity is not None else 0

        filtered_df = filtered_df.dropna(subset=[season_column], how='any')
        filtered_df = filtered_df[filtered_df[season_column] != 'None']

        filtered_df[[season_column]] = filtered_df[[season_column]].apply(
            pd.to_numeric, errors='coerce'
        )

        if not filtered_df.empty and 'variety' in filtered_df.columns:
            selected_variety = filtered_df.loc[
                abs(filtered_df[season_column] - days_to_maturity).idxmin(), 'variety'
            ]
        else:
            selected_variety = None
            # print("No valid variety for the selected features and season.")

        return selected_variety

# Example user inputs
# These will be replaced by the values received from the HTML form in the Flask app
type_selection = "OPV Glutinous Corn"
trait_selection = "White"
domain_selection = "Visayas"
planting_date_selection = "2023-11-01"
target_harvest_date_selection = "2024-03-01"

# Assuming df is a CSV loaded DataFrame
csv_path = 'corn.csv'
tree_model = C45DecisionTree(csv_path)

# Predict variety
predicted_variety, filtered_df, days_to_maturity = tree_model.predict_variety(
    type_selection, trait_selection, domain_selection, planting_date_selection, target_harvest_date_selection
)

if predicted_variety is not None:
    # print(f"The predicted corn variety is: {predicted_variety}")

    # Convert planting and harvest dates to datetime
    planting_date_selection = tree_model.convert_date(planting_date_selection)
    target_harvest_date_selection = tree_model.convert_date(target_harvest_date_selection)

    # Calculate number of days to maturity
    days_to_maturity = tree_model.calculate_days_to_maturity(planting_date_selection, target_harvest_date_selection)

    # Determine season
    season = tree_model.determine_season(planting_date_selection)

    # Select variety based on maturity_ds
    tree_model.select_variety(filtered_df, days_to_maturity, 'maturity_ds', planting_date_selection, target_harvest_date_selection, season)

    # Select variety based on maturity_ws
    tree_model.select_variety(filtered_df, days_to_maturity, 'maturity_ws', planting_date_selection, target_harvest_date_selection, season)
else:
    print("No valid variety for the selected features and season.")

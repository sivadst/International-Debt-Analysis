import pandas as pd
import numpy as np
import os
import random

def generate_mock_data(output_path):
    print("Generating mock international debt data...")
    
    # Predefined lists of countries and indicators based on typical World Bank IDS dataset
    countries = [
        "Afghanistan", "Albania", "Algeria", "Angola", "Argentina", 
        "Armenia", "Bangladesh", "Belarus", "Belize", "Benin",
        "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil",
        "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
        "Cameroon", "Central African Republic", "Chad", "China", "Colombia",
        "Comoros", "Congo, Dem. Rep.", "Congo, Rep.", "Costa Rica", "Cote d'Ivoire",
        "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt, Arab Rep.",
        "El Salvador", "Eritrea", "Eswatini", "Ethiopia", "Fiji",
        "Gabon", "Gambia, The", "Georgia", "Ghana", "Grenada",
        "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
        "Honduras", "India", "Indonesia", "Iran, Islamic Rep.", "Jamaica",
        "Jordan", "Kazakhstan", "Kenya", "Kosovo", "Kyrgyz Republic",
        "Lao PDR", "Lebanon", "Lesotho", "Liberia", "Madagascar",
        "Malawi", "Maldives", "Mali", "Mauritania", "Mauritius",
        "Mexico", "Moldova", "Mongolia", "Montenegro", "Morocco",
        "Mozambique", "Myanmar", "Nepal", "Nicaragua", "Niger",
        "Nigeria", "North Macedonia", "Pakistan", "Papua New Guinea", "Paraguay",
        "Peru", "Philippines", "Rwanda", "Samoa", "Sao Tome and Principe",
        "Senegal", "Serbia", "Sierra Leone", "Solomon Islands", "Somalia",
        "South Africa", "Sri Lanka", "St. Lucia", "St. Vincent and the Grenadines", "Sudan",
        "Syrian Arab Republic", "Tajikistan", "Tanzania", "Thailand", "Togo",
        "Tonga", "Tunisia", "Turkey", "Turkmenistan", "Uganda",
        "Ukraine", "Uzbekistan", "Vanuatu", "Venezuela, RB", "Vietnam",
        "Yemen, Rep.", "Zambia", "Zimbabwe"
    ]
    
    # 20 distinct debt indicators
    indicators = [
        ("Principal repayments on external debt, long-term (AMT, current US$)", "DT.AMT.DLXF.CD"),
        ("Principal repayments on external debt, private nonguaranteed (PNG) (AMT, current US$)", "DT.AMT.DPNG.CD"),
        ("Principal repayments on external debt, public and publicly guaranteed (PPG) (AMT, current US$)", "DT.AMT.DPPG.CD"),
        ("Disbursements on external debt, long-term (DIS, current US$)", "DT.DIS.DLXF.CD"),
        ("Disbursements on external debt, private nonguaranteed (PNG) (DIS, current US$)", "DT.DIS.DPNG.CD"),
        ("Disbursements on external debt, public and publicly guaranteed (PPG) (DIS, current US$)", "DT.DIS.DPPG.CD"),
        ("Interest payments on external debt, long-term (INT, current US$)", "DT.INT.DLXF.CD"),
        ("Interest payments on external debt, private nonguaranteed (PNG) (INT, current US$)", "DT.INT.DPNG.CD"),
        ("Interest payments on external debt, public and publicly guaranteed (PPG) (INT, current US$)", "DT.INT.DPPG.CD"),
        ("Net flows on external debt, private nonguaranteed (PNG) (NFL, current US$)", "DT.NFL.DPNG.CD"),
        ("Net flows on external debt, public and publicly guaranteed (PPG) (NFL, current US$)", "DT.NFL.DPPG.CD"),
        ("Commitments, public and publicly guaranteed (COM, current US$)", "DT.COM.DPPG.CD"),
        ("External debt stocks, long-term (DOD, current US$)", "DT.DOD.DLXF.CD"),
        ("External debt stocks, private nonguaranteed (PNG) (DOD, current US$)", "DT.DOD.DPNG.CD"),
        ("External debt stocks, public and publicly guaranteed (PPG) (DOD, current US$)", "DT.DOD.DPPG.CD"),
        ("External debt stocks, short-term (DOD, current US$)", "DT.DOD.DSTC.CD"),
        ("External debt stocks, total (DOD, current US$)", "DT.DOD.DECT.CD"),
        ("Net transfers on external debt, private nonguaranteed (PNG) (NTR, current US$)", "DT.NTR.DPNG.CD"),
        ("Net transfers on external debt, public and publicly guaranteed (PPG) (NTR, current US$)", "DT.NTR.DPPG.CD"),
        ("Net transfers on external debt, total (NTR, current US$)", "DT.NTR.DECT.CD")
    ]
    
    # We will generate data for years 2010 to 2021
    years = list(range(2010, 2022))
    
    data = []
    
    # Seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    for country in countries:
        # Base debt scale for the country (richer/larger countries have more debt)
        scale = np.random.lognormal(mean=20, sigma=1.5)
        
        # Each country might not have all indicators (missing data)
        num_indicators = random.randint(15, len(indicators))
        country_indicators = random.sample(indicators, num_indicators)
        
        for ind_name, ind_code in country_indicators:
            # We create a record per year to make a rich dataset, but the original dataset often has them as columns.
            # To match the "CSV to DataFrame Conversion" and cleaning needs, we'll format it with years as columns or long format.
            # Usually, World Bank data has Country Name, Country Code, Indicator Name, Indicator Code, 1970, 1971... 2021
            row = {
                "Country Name": country,
                "Country Code": country[:3].upper() if len(country) > 3 else country.upper(),
                "Indicator Name": ind_name,
                "Indicator Code": ind_code
            }
            
            # Indicator specific scale factor
            if "total" in ind_name.lower():
                ind_scale = 1.0
            elif "public" in ind_name.lower():
                ind_scale = 0.6
            elif "private" in ind_name.lower():
                ind_scale = 0.3
            elif "interest" in ind_name.lower():
                ind_scale = 0.05
            else:
                ind_scale = 0.1
                
            base_val = scale * ind_scale
            
            for year in years:
                # Add some random growth/variance
                year_val = base_val * (1 + (year - 2010) * 0.05) * np.random.uniform(0.8, 1.2)
                
                # Introduce some missing values randomly (approx 5%)
                if random.random() < 0.05:
                    row[str(year)] = np.nan
                else:
                    row[str(year)] = year_val
                    
            data.append(row)
            
    df = pd.DataFrame(data)
    
    # Introduce some full duplicate rows to satisfy the cleaning requirement
    duplicates = df.sample(n=int(len(df) * 0.02), replace=True, random_state=42)
    df = pd.concat([df, duplicates], ignore_index=True)
    
    # Shuffle dataset
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Mock data generated successfully and saved to {output_path}")
    print(f"Shape: {df.shape}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "../data/raw/international_debt.csv")
    if not os.path.exists(output_path):
        generate_mock_data(output_path)
    else:
        print(f"File already exists at {output_path}")

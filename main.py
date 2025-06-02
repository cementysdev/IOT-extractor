from src.extractor import extract_data, filter_excel_rows

def main():
    begin_date = "2025-03-30 18:00:00+01:00"
    end_date = "2025-03-31 08:00:00+01:00"

    #df = extract_data(devEUI, begin_date, end_date)
    df_filtered = filter_excel_rows(
        "~/OneDrive - SOCOTEC S.A\General - Equipe IoT\\03 - Fonctionnement Fablab\\08 - Suivi IoT\\SMF.SuiviIoT.V3.xlsx",
        sheet_name="CapteurList",
        column_name="Emplacement",
        condition_func=lambda x: x == "SO24090003-T"
    )
    print(df_filtered)

    devEUI = df_filtered['DevEUI'].tolist()
    df = extract_data(devEUI, begin_date, end_date)
    print(df)


if __name__ == "__main__":
    main()

from src.extractor import extract_data

def main():
    devEUI = ["bbbb000001004050", "bbbb000001002932"]
    begin_date = "2025-03-30 18:00:00+01:00"
    end_date = "2025-03-31 08:00:00+01:00"

    df = extract_data(devEUI, begin_date, end_date)
    print(df)


if __name__ == "__main__":
    main()

from frontend import ExcelValidatorUI
from backend import process_excel, excel_to_sql
import logging
import sentry_sdk

sentry_sdk.init(
    dsn="https://c1a0ce2c70a4f2376d6f2daefdcd21d2@o4507863466508288.ingest.us.sentry.io/4507863468670976",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)
def main():
    ui = ExcelValidatorUI()
    ui.display_header()

    upload_file = ui.upload_file()

    if upload_file:
        df, result, erros = process_excel(upload_file)
        ui.display_results(result, erros)

        if erros:
            ui.display_wrong_message()
            logging.error("Planilha com erro de Schema")
            sentry_sdk.capture_message("A planilha estava errada")
        elif ui.display_save_button():
            excel_to_sql(df)
            ui.display_success_message()
            logging.info("Foi enviado com sucesso ao banco SQL")
            sentry_sdk.capture_message("O banco SQL foi atualizado")




if __name__ == "__main__":
    main()
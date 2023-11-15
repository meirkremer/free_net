import smtplib
from email.mime.text import MIMEText
from db_client import daily_summary
from config import private_config as conf


def create_report():
    text_report = 'daily report:\n'
    daily_data = daily_summary()

    search_data = daily_data.get('search_data')
    download_data = daily_data.get('download_data')

    sum_size = sum([item.get('file_size') for item in download_data.values()]) / 1024 ** 3

    text_report += f'sum searches for last day: {len(search_data)}\n'
    text_report += f'sum downloads for last day: {len(download_data)}\nall files size: {sum_size:.3f} GB\n\n\n'

    text_report += f'search details:\n{"~" * len("search details:")}\n'
    for search in search_data:
        search_item = search_data[search]
        text_report += f'search id: {search}\nuser name: {search_item.get("user_name")}\n' \
                       f'query: {search_item.get("search_query")}\ndatetime: {search_item.get("date")}\n\n'

    text_report += f'\n\n\ndownload details:\n{"~" * len("download details:")}\n'
    for download in download_data:
        download_item = download_data[download]
        text_report += f"download id: {download}\nuser name: {download_item.get('user_name')}\n" \
                       f"file name: {download_item.get('file_name')}\n" \
                       f"file size: {(download_item.get('file_size') / 1024 ** 3):.3f} GB\n" \
                       f"datetime: {download_item.get('date')}\n\n"

    return text_report


def send_report():
    from_email = conf['sender_email']
    to_email = 'marworm1@gmail.com'
    subject = 'FreeNet Daily Report'
    message = create_report()

    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()  # Use TLS for secure communication
        server.login(from_email, conf['email_password'])
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print('Email sent successfully')
    except Exception as e:
        print('Email could not be sent. Error:', str(e))


if __name__ == '__main__':
    send_report()

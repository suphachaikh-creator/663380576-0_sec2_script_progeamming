# Week 12 LabX Advanced: Agentic Communication Workflows

## Goal
Build a configuration-driven email/SMS agent. It sends a templated sales report, creates an incoming request message, searches the inbox, downloads matching attachments, and applies rules to send an alert or reply.

## Setup
1. Install Python 3.10+ and dependencies:
   ```powershell
   py -m pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` in this project folder.
3. Fill in Gmail's SMTP/IMAP settings and a Google App Password. Never commit or share `.env`.
4. Edit `configs/comm_pipeline_config.json`: replace every example recipient, sender filter, and SMS gateway address with values appropriate to your setup. The supplied carrier gateways are US carrier email gateways; they generally will not deliver to Thai mobile numbers.
5. Sample `sales_report.pdf` and `summary_data.xlsx` files are included under `data/reports/` for preview. Replace them with your real report files before live sending, or change the attachment paths in the config.

## Run safely
The supplied `.env.example` sets `DRY_RUN=true`, which simulates the three workflow steps without connecting to Gmail or sending email/SMS. Copy it to `.env`, then run from any folder:
```powershell
py "C:\path\to\Week_12_LabX_ADV_Agentic_Communication_Workflows_Advanced_Email_And_SMS-main\main.py"
```
The generated audit JSON is saved under `reports/`; downloaded attachments go under `data/incoming_attachments/`.

To enable live sending, first replace all example addresses and review every task in the JSON configuration. Then set `DRY_RUN=false` in `.env`. Live mode sends the configured emails and SMS and reads the configured mailbox.

For the email screenshot deliverable, enter your App Password locally in .env, set DRY_RUN=false, and run only the report email task:
    py main.py --task "Send Daily Sales Report Email"

This sends one report email to the configured recipient and skips the SMS and inbox-processing tasks.

## Workflow tasks
- **Send Daily Sales Report Email**: renders date, sales, and customer count placeholders and attaches configured reports.
- **Simulate Incoming Request Email**: sends a request message to the configured mailbox.
- **Process Incoming Data Requests**: searches unread inbox messages by sender and subject, downloads attachments, then matches rules for SMS alerts and email replies.

Templates can use context keys such as `{report_date}`, `{sales_figure:.2f}`, `{total_customers}`, `{sender}`, and `{subject}`.

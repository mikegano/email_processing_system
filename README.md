# Email Processing System

A Python-based email processing system designed to handle, filter, and process incoming emails from multiple sources. Customize scraping and data extraction to automate your email workflows and integrate seamlessly with tools like Notion.

![GitHub issues](https://img.shields.io/github/issues/mikegano/email_processing_system)
![GitHub license](https://img.shields.io/github/license/mikegano/email_processing_system)

## Features

- **Multi-Source Email Processing:** Handle emails from various providers.
- **Customizable Extraction:** Define what data to scrape and how to process it.
- **Lightweight and Configurable:** Easy setup with minimal dependencies.
- **Notion Integration:** Optionally integrate with Notion to store and organize data.
- **Extensible Architecture:** Designed with modularity in mind for future enhancements.

## Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package installer)

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/mikegano/email_processing_system.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd email_processing_system
   ```

3. **Create a virtual environment (recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

4. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, you need to configure it:

1. **Environment Variables:**

   Create a `.env` file in the project root directory:

   ```env
   EMAIL_SERVER=your_email_server
   EMAIL_PORT=your_email_port
   EMAIL_USERNAME=your_email_username
   EMAIL_PASSWORD=your_email_password
   ```

2. **Notion Integration (optional):**

   Add the following to your `.env` file if using Notion:

   ```env
   NOTION_TOKEN=your_notion_token
   NOTION_DATABASE_ID=your_notion_database_id
   ```

## Usage

1. **Activate the virtual environment:**

   ```bash
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Run the application:**

   ```bash
   python -m app.main
   ```

   This will start processing emails using your configuration settings.

## Contributing

We welcome contributions to this project! Here's how you can help:

1. **Fork the Repository:**

   Click the "Fork" button at the top right corner of the repository page to create your own copy.

2. **Clone Your Fork:**

   Replace `your-username` with your GitHub username:

   ```bash
   git clone https://github.com/your-username/email_processing_system.git
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes and Commit:**

   ```bash
   git commit -m 'Add your feature'
   ```

5. **Push to Your Fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a Pull Request:**

   Go to your fork on GitHub and click the "New Pull Request" button.

## Roadmap

- [ ] Don't add listing if they're duplicates.
- [ ] Add more job listing sites (and their parsers).
- [ ] Add support for IMAP email retrieval.
- [ ] Implement OAuth 2.0 support for Gmail.
- [ ] Add support for IMAP email retrieval.
- [ ] Integrate AI for generating the parsing files.
- [ ] Develop a web interface for configuration and monitoring.

## Support

If you have any questions or need assistance, please open an issue on GitHub or contact me at [mikejgano@gmail.com](mailto:mikejgano@gmail.com).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

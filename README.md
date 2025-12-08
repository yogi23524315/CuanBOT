# CuanBOT



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

* [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
* [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/mail.yogipratama-group/cuanbot.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

* [Set up project integrations](https://gitlab.com/mail.yogipratama-group/cuanbot/-/settings/integrations)

## Collaborate with your team

* [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
* [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
* [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
* [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
* [Set auto-merge](https://docs.gitlab.com/user/project/merge_requests/auto_merge/)

## Test and Deploy

Use the built-in continuous integration in GitLab.

* [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/)
* [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
* [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
* [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
* [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README

Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

<<<<<<< HEAD
## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
=======
## 📱 Cara Menggunakan Bot

### Mencatat Transaksi

Cukup chat dengan bahasa natural:

```
✅ "Terima pembayaran dari customer 500rb"
✅ "Bayar listrik 300 ribu"
✅ "Piutang si Budi 1 juta"
✅ "Hutang ke supplier 2 juta untuk stok barang"
✅ "Dapat transfer dari customer A sebesar 1.5 juta untuk pembelian produk X"
```

### Commands

- `/start` - Mulai bot & lihat panduan
- `/help` - Bantuan lengkap
- `/summary` - Ringkasan keuangan Anda

### Bertanya

```
"Bagaimana cara menghitung laba rugi?"
"Apa itu arus kas?"
"Jelaskan tentang piutang dan hutang"
```

## 🎨 Dashboard Features

### 1. Overview Cards
- Total Pemasukan
- Total Pengeluaran
- Saldo
- Jumlah Transaksi

### 2. Charts & Analytics
- **Daily Transaction Chart**: Trend harian income vs expense
- **Category Breakdown**: Pie chart pengeluaran per kategori
- **Revenue Forecast**: Prediksi 30 hari ke depan (ML)
- **Anomaly Detection**: Transaksi mencurigakan (ML)

### 3. Bot Monitoring
- Real-time logs
- Activity tracking
- Error monitoring

## 🔧 Development

### Project Structure

```
CuanBOTv3/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic
│   │   │   ├── telegram_bot.py
│   │   │   ├── llm_service.py
│   │   │   ├── ml_forecasting.py
│   │   │   └── ml_anomaly.py
│   │   ├── api/               # REST API endpoints
│   │   └── main.py            # FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
│
├── dashboard/                  # Next.js Dashboard
│   ├── src/
│   │   ├── app/               # Next.js 14 App Router
│   │   ├── components/        # React components
│   │   └── lib/               # Utilities & API client
│   ├── package.json
│   └── Dockerfile
│
├── init-db/                    # Database initialization
│   └── init.sql
│
├── docker-compose.yml          # Docker orchestration
├── .env.example               # Environment template
└── README.md
```

### Running Locally (Development)

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Dashboard:**
```bash
cd dashboard
npm install
npm run dev
```

### API Documentation

Setelah backend running, akses:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

### Manual Testing Telegram Bot

1. Start bot dengan `/start`
2. Test pencatatan transaksi:
   ```
   "Terima uang 500rb dari customer"
   "Bayar gaji 2 juta"
   ```
3. Check dengan `/summary`

### Testing Dashboard

1. Access http://localhost:3000
2. Verify semua cards menampilkan data
3. Test ML features:
   - Click "Generate Forecast"
   - Click "Detect Anomalies"

## 📊 Database Schema

### Tables

- **users**: Telegram user data
- **transactions**: Financial transactions
- **bot_logs**: Bot interaction logs
- **predictions**: ML prediction results

## 🔐 Security Notes

⚠️ **Important for Production:**

1. Change all default passwords
2. Use strong SECRET_KEY
3. Enable HTTPS for webhook
4. Implement authentication for dashboard
5. Add rate limiting
6. Regular database backups

## 🐛 Troubleshooting

### Webhook Issues

```bash
# Check ngrok status
curl http://localhost:4040/api/tunnels

# Manually set webhook
curl -X POST "https://api.telegram.org/bot<TOKEN>/setWebhook?url=<NGROK_URL>/webhook/telegram"
```

### Database Connection Issues

```bash
# Check PostgreSQL
docker-compose exec postgres psql -U cuanbot -d cuanbot_db -c "\dt"

# Reset database
docker-compose down -v
docker-compose up -d
```

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f dashboard
```

## 🚀 Deployment (Production)

### Quick Deploy to ubuntu@vm-4-97-ubuntu

```bash
cd deployment
cp .env.example .env
nano .env  # Configure your production credentials
./deploy-to-server.sh latest
```

**Complete Deployment Documentation:**
- 📖 [deployment/DEPLOY_README.md](deployment/DEPLOY_README.md) - Step-by-step deployment guide
- ⚡ [deployment/QUICK_REFERENCE.md](deployment/QUICK_REFERENCE.md) - Quick reference commands
- ✅ [deployment/DEPLOYMENT_CHECKLIST.md](deployment/DEPLOYMENT_CHECKLIST.md) - Deployment checklist

**Management Commands:**
```bash
./server-commands.sh logs      # View logs
./server-commands.sh status    # Check status
./server-commands.sh restart   # Restart services
./server-commands.sh backup    # Backup database
./server-commands.sh monitor   # Real-time monitoring
```

### Using Docker Compose (Manual)

1. Update `.env` dengan production credentials
2. Use production-grade secrets
3. Setup proper domain & SSL
4. Use managed PostgreSQL (e.g., AWS RDS, Google Cloud SQL)
5. Deploy to cloud (AWS, GCP, Azure)

### Recommendations

- Use Kubernetes for scalability
- Implement CI/CD pipeline
- Setup monitoring (Prometheus, Grafana)
- Add backup automation
- Implement proper logging (ELK stack)

## 📝 License

MIT License

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ for Indonesian UMKM**
# CuanBOT
>>>>>>> 3753bb1 (first commit)

# iGOT Backend

Backend server for the SIH iGOT MVP: competency gap engine + quiz generation + iGOT stub.

## Stack

- Fastify (TypeScript)
- MongoDB (Mongoose)
- OpenAI API (quiz generation, embeddings)
- Zod (validation)

## Setup

```bash
npm install
cp .env.example .env
# fill in MONGO_URI, OPENAI_API_KEY, JWT_SECRET in .env
npm run dev
```

Server starts on `http://localhost:5000` (or your `PORT`). Check `GET /health` to confirm it's running.

## Structure

```
src/
├── config/        # env + db connection
├── modules/
│   ├── auth/        # user/admin, roles
│   ├── material/    # upload + PDF/text extraction
│   ├── quiz/         # quiz generation via LLM
│   ├── competency/   # gap analysis + recommendations
│   └── igot/          # iGOT integration (mocked for now)
├── app.ts         # fastify app builder
└── server.ts      # entry point
```

## Scripts

- `npm run dev` — start in watch mode
- `npm run build` — compile TypeScript to `dist/`
- `npm start` — run compiled build

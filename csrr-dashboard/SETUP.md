# CSRR Mailing List Dashboard Setup

This guide will help you set up the CSRR Faculty Media Reports mailing list dashboard with Supabase backend.

## Prerequisites

- Node.js (version 14 or higher)
- A Supabase account (free tier is sufficient)

## Step 1: Set up Supabase Database

1. **Create a Supabase project:**
   - Go to [supabase.com](https://supabase.com)
   - Sign up/Sign in and create a new project
   - Note down your project URL and API keys

2. **Create the mailing list table:**
   - Go to the SQL Editor in your Supabase dashboard
   - Run this SQL to create the table:

```sql
-- Create mailing_list table
CREATE TABLE mailing_list (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    organization VARCHAR(255),
    title VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE mailing_list ENABLE ROW LEVEL SECURITY;

-- Create policy to allow inserts from anyone
CREATE POLICY "Allow public inserts" ON mailing_list
    FOR INSERT TO anon
    WITH CHECK (true);

-- Create policy to allow select for authenticated users
CREATE POLICY "Allow select for authenticated users" ON mailing_list
    FOR SELECT TO authenticated
    USING (true);
```

3. **Get your credentials:**
   - Go to Settings → API
   - Copy your Project URL
   - Copy your `anon` (public) key
   - Copy your `service_role` (secret) key

## Step 2: Configure the React App

1. **Install dependencies:**
   ```bash
   cd csrr-dashboard
   npm install
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file:**
   ```
   REACT_APP_SUPABASE_URL=your_supabase_project_url
   REACT_APP_SUPABASE_ANON_KEY=your_supabase_anon_key
   ```

## Step 3: Configure the Export Script

1. **Install Python dependencies:**
   ```bash
   pip install supabase pandas openpyxl python-dotenv
   ```

2. **Create a `.env` file in the main project directory:**
   ```
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_SERVICE_KEY=your_supabase_service_role_key
   ```

## Step 4: Run the Dashboard

```bash
cd csrr-dashboard
npm start
```

The dashboard will be available at `http://localhost:3000`

## Step 5: Export Subscribers

To get an Excel file of all subscribers for your monthly reports:

```bash
python3 export_subscribers.py
```

This will create an Excel file with all subscriber information.

## Monthly Workflow

1. **Run your media search automation:**
   ```bash
   python3 csrr_production_search.py
   ```

2. **Export subscriber list:**
   ```bash
   python3 export_subscribers.py
   ```

3. **Use the Excel file to send monthly reports to all subscribers**

## Security Notes

- The dashboard allows anyone to sign up (by design)
- The admin view requires manual activation (click the "Show Subscriber List" button)
- For production deployment, consider adding authentication for the admin features
- Keep your service role key secure and never expose it in client-side code

## Deployment

For production deployment, you can:

1. **Deploy to Vercel (recommended for React apps):**
   - Connect your GitHub repo to Vercel
   - Add environment variables in Vercel dashboard
   - Deploy automatically

2. **Deploy to Netlify:**
   - Similar process to Vercel
   - Add environment variables in Netlify dashboard

3. **Deploy to any static hosting service**

## Troubleshooting

- **"Missing environment variables" error:** Make sure your `.env` files are properly configured
- **Database connection errors:** Verify your Supabase URL and keys
- **Signup not working:** Check that RLS policies are set up correctly
- **Export script failing:** Ensure you have the service role key, not the anon key

## Support

For technical issues, check:
1. Supabase dashboard for database errors
2. Browser console for client-side errors
3. Ensure all environment variables are set correctly

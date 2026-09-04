import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY;

const projectUrl = supabaseUrl?.replace(/\/rest\/v1\/?$/, "").replace(/\/$/, "");

export const supabase = createClient(
  projectUrl,
  supabaseKey
);
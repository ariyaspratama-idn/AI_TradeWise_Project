import os
import random
# In a real scenario, we would import openai, anthropic, google.generativeai

class MultiAIModel:
    def __init__(self):
        self.models = {
            "gpt-4o": self._call_gpt,
            "gemini-flash-latest": self._call_gemini, # Updated key
            "gemini-pro": self._call_gemini        # Backwards compatibility
        }
        self.default_model = "gpt-4o"

# ... (skip to _call_gemini)

    def _call_gemini(self, prompt, context):
        """Call Google Gemini API implementation."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return "[System] Error: GOOGLE_API_KEY belum diset di .env."

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            
            # Use newer model
            model = genai.GenerativeModel('gemini-flash-latest')
            
            # Gabungkan system prompt ke user prompt karena Gemini Pro basic tidak selalu support parameter system terpisah di versi lama
            full_prompt = f"Role: Anda adalah AI TradeWise. Data Pasar: {context}\n\nPertanyaan: {prompt}"
            
            response = model.generate_content(full_prompt)
            return response.text
        except ImportError:
            return "[System] Error: Library 'google-generativeai' belum terinstall. Jalankan: pip install google-generativeai"
        except Exception as e:
            return f"[API Error] Masalah koneksi ke Google Gemini: {str(e)}"

    def generate_response(self, prompt, context=None, model_name=None):
        """
        Smart Generate:
        1. Jika model_name spesifik diminta, gunakan itu.
        2. Jika 'auto' atau None, coba OpenAI (Premium) dulu.
        3. Jika OpenAI gagal (limit/error), otomatis fallback ke Gemini (Free).
        """
        
        # Jika user minta spesifik (misal dari tes lama), layani
        if model_name and model_name != "auto" and model_name in self.models:
            return self.models[model_name](prompt, context)

        # Logic Auto-Pilot: Prioritas OpenAI -> Fallback Gemini
        try:
            # Coba OpenAI dulu
            print("[Auto-Pilot] Mencoba OpenAI GPT-4o...")
            response = self._call_gpt(prompt, context)
            
            # Cek apakah response berisi pesan error sistem kita sendiri (yg diawali [API Error] atau ⚠️)
            # Karena _call_gpt me-return string error, bukan raise exception Python murni di level ini
            if response.startswith("[API Error]") or response.startswith("⚠️") or "[System]" in response:
                raise Exception("OpenAI Error Detected in Response")
                
            return response + "\n\n*(Dijawab oleh OpenAI)*"
            
        except Exception:
            # Fallback ke Gemini
            print("[Auto-Pilot] OpenAI Gagal/Limit, beralih ke Gemini...")
            try:
                gemini_response = self._call_gemini(prompt, context)
                return gemini_response #+ "\n\n*(Dijawab oleh Gemini - Fallback)*"
            except Exception as e:
                return f"[System Fatal] Semua AI sibuk/error. Terakhir: {str(e)}"

    def _call_gpt(self, prompt, context):
        """Call OpenAI GPT-4o API real implementation."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or "sk-" not in api_key:
            return "[System] Info: OpenAI belum dikonfigurasi. Silakan pilih 'Google Gemini' di menu dropdown atas."
        
        try:
            from openai import OpenAI
            import httpx
            
            # Fix: Create explicit http_client to avoid auto-proxy kwargs issues
            http_client = httpx.Client()
            client = OpenAI(api_key=api_key, http_client=http_client)
            
            # Bangun konteks sistem
            system_msg = "Anda adalah AI TradeWise, asisten trading profesional. Analisis data pasar yang diberikan dan berikan saran yang objektif, namun ingatkan risiko trading."
            if context:
                system_msg += f"\nData Pasar Terkini: {context}"

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return response.choices[0].message.content
        except ImportError:
            return "[System] Error: Library 'openai' tidak terinstall."
        except Exception as e:
            error_msg = str(e)
            if "insufficient_quota" in error_msg or "429" in error_msg:
                return "⚠️ **Anda sudah sampai limit.** Silakan pindah ke **Google Gemini Flash**."
            
            # Fallback friendly message
            return f"[API Error] Masalah koneksi ke OpenAI ({error_msg}). \nSARAN: Coba pilih 'Google Gemini Flash' di dropdown atas, itu gratis & lebih stabil."

    def _call_claude(self, prompt, context):
        """Call Anthropic Claude 3 API implementation."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return "[System] Error: ANTHROPIC_API_KEY belum diset di .env."
            
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            
            system_msg = "Anda adalah AI TradeWise, analis pasar senior. Berikan insight mendalam."
            if context:
                system_msg += f"\nData Pasar: {context}"

            message = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=300,
                temperature=0.7,
                system=system_msg,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
        except ImportError:
            return "[System] Error: Library 'anthropic' belum terinstall. Jalankan: pip install anthropic"
        except Exception as e:
            return f"[API Error] Masalah koneksi ke Anthropic: {str(e)}"




# Añadir temporalmente al inicio de main() para diagnosticar
def diagnosticar_audio():
    st.sidebar.write("🔧 Diagnóstico Audio")
    if st.sidebar.button("Probar Sistema"):
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.say("Prueba básica")
            engine.runAndWait()
            st.sidebar.success("pyttsx3 funcionando")
        except Exception as e:
            st.sidebar.error(f"Error pyttsx3: {e}")
            
            # Fallback Windows
            import os, platform
            if platform.system() == "Windows":
                try:
                    os.system('powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak(\'Prueba PowerShell\')"')
                    st.sidebar.success("PowerShell funcionando")
                except:
                    st.sidebar.error("PowerShell también falló")

# Llamar antes de las pestañas
diagnosticar_audio()
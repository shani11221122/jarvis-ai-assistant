import speech_recognition as sr
import webbrowser
import pyttsx3
import music
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "8a611a9b564249048282190c16d2fd82"


def speak(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    while True:
        speak("Initial Jarvis")
        r = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)

            text = r.recognize_google(audio)
            print(f"You said: {text}")
            text_lower = text.lower()

            # --- EXIT Commands ---
            if any(word in text_lower for word in ["stop", "exit", "quit", "close", "bye", "goodbye"]):
                speak("Goodbye Zeeshan! Have a great day!")
                break

            # --- PLAY MUSIC ---
            elif text_lower.startswith("play music"):
                song = text_lower.split("play music", 1)[1].strip()
                if song:
                    link = music.musics.get(song)
                    if not link:
                        # Try alternate mapping if number
                        alt_song = {"1": "one", "2": "two",
                            "3": "three"}.get(song)
                        if alt_song:
                            link = music.musics.get(alt_song)

                    if link:
                        webbrowser.open(link)
                        speak(f"Playing {song}")
                    else:
                        speak("Sorry, I don't have that song in my library.")
                else:
                    speak("Please specify a song to play.")
                continue

            # --- OPEN WEBSITE ---
            elif "open" in text_lower:
                website = text_lower.replace("open", "").strip()
                if "google" in website:
                    url = "https://www.google.com"
                elif "youtube" in website:
                    url = "https://www.youtube.com"
                elif "facebook" in website:
                    url = "https://www.facebook.com"
                elif "twitter" in website:
                    url = "https://www.twitter.com"
                elif "instagram" in website:
                    url = "https://www.instagram.com"
                elif "linkedin" in website:
                    url = "https://www.linkedin.com"
                elif "github" in website:
                    url = "https://www.github.com"
                else:
                    if website.startswith("www."):
                        url = f"https://{website}"
                    else:
                        url = f"https://{website}.com"
                webbrowser.open(url)
                speak(f"Opening {website}")
                continue

            # --- NEWS HEADLINES ---
            elif "news" in text_lower:
                try:
                    speak("Fetching the latest news headlines...")
                    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
                    response = requests.get(url)
                    data = response.json()

                    if data["status"] == "ok":
                        articles = data["articles"][:5]
                        for i, article in enumerate(articles, start=1):
                            headline = article["title"]
                            print(f"{i}. {headline}")
                            speak(f"Headline {i}: {headline}")
                    else:
                        speak("Sorry, I couldn't fetch the news right now.")
                except Exception as e:
                    print("Error while fetching news:", e)
                    speak("There was an error getting the news.")
                continue
         
    
          
            else:
                speak("I can only open websites, play music, or get news. Try saying 'open YouTube', 'play music one', or 'news'.")
                continue

    
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            speak("Sorry, I did not understand that.")
        except sr.WaitTimeoutError:
            print("Timeout error. You were silent.")
            speak("You stayed silent. Try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("Could not request results.")
        except Exception as e:
            print(f"Error: {e}")
            speak("Something went wrong.")

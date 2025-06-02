import sys
import requests
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel,QVBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # self.setGeometry(600,250,500,500)

        self.city_label= QLabel("Enter City Name",self)
        self.cityinput= QLineEdit(self)
        self.button=QPushButton("Get Weather", self)
        self.temprature=QLabel(self)
        self.emoji_level= QLabel(self)
        self.decripition_level=QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox= QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.cityinput)
        vbox.addWidget(self.button)
        vbox.addWidget(self.temprature)
        vbox.addWidget(self.emoji_level)
        vbox.addWidget(self.decripition_level)
        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.cityinput.setAlignment(Qt.AlignCenter)
        self.temprature.setAlignment(Qt.AlignCenter)
        self.emoji_level.setAlignment(Qt.AlignCenter)
        self.decripition_level.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.cityinput.setObjectName("city_input")
        self.button.setObjectName("get_weather_button")
        self.temprature.setObjectName("temprature")
        self.emoji_level.setObjectName("emoji_level")
        self.decripition_level.setObjectName("decripition_level")

        self.setStyleSheet("""
                        QLabel, QPushButton{
                           font-family:calibri;
                           }
                        QLabel#city_label{
                           font-size:40px;
                           font-style: italic ; 
                           }
                        QLineEdit#city_input{
                           font-size:40px;
                           }
                        QPushButton#get_weather_button{
                           font-size :30px ;
                           font-weight : bold ;
                           }
                        QLabel#temprature{
                           font-size:75px;
                           }
                        QLabel#emoji_level{
                           font-size:150px;
                           font-family:Segoe UI Emoji;
                           }
                        QLabel#decripition_level{
                           font-size:100px;
                           }

                            """)
        self.button.clicked.connect(self.get_weather)
        

    def get_weather(self):
        
        api_key="6d509b08ad818716735ee562bf0771de"
        city=self.cityinput.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:    
        
            response=requests.get(url)
            response.raise_for_status()
            data=response.json()

            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error: 
            match response.status_code: 
                case 400: 
                    self.display_error("Bad request: \nPlease check your input") 
                case 401: 
                    self.display_error("Unauthorized:\nInvalid API key") 
                case 403: 
                    self.display_error("Forbidden: \nAccess is denied") 
                case 404: 
                    self.display_error("Not found: \nCity not found") 
                case 500: 
                    self.display_error("Internal Server Error: \nPlease try again later") 
                case 502: 
                    self.display_error("Bad Gateway: \nInvalid response from the server")   
                case 503: 
                    self.display_error("Service UnavailableinServer is down") 
                case 504: 
                    self.display_error("Gateway Timeout:\nNo response from the server")  
                case _: 
                    self.display_error(f"HTTP error occurred:\n{http_error}")   

        except requests.exceptions.ConnectionError: 
            self.display_error("Connection Error: \nCheck your internet connection") 
        except requests.exceptions.Timeout: 
            self.display_error("Timeout Error: \nThe request timed out") 
        except requests.exceptions.TooManyRedirects: 
            self.display_error("Too many Redirects: \nCheck the URL") 
        except requests.exceptions.RequestException as req_error:             
            self.display_error(f"Request Error: \n{req_error}")  


    def display_error(self,message):
        self.temprature.setStyleSheet("font-size:30px;")
        self.temprature.setText(message)
        self.emoji_level.setText("")
        self.decripition_level.setText("")


    def display_weather(self,data):
        
        tem=data['main']['temp']
        tem_c=tem-273.15
        descrp=data['weather'][0]['description']
        weather_id=data['weather'][0]['id']

        self.temprature.setText(f"{tem_c:.0f}°C")
        self.emoji_level.setText(self.get_emoji(weather_id))
        self.decripition_level.setText(f"{descrp.capitalize()}")
        

    @staticmethod
    def get_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701<= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""




def main():
    app= QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
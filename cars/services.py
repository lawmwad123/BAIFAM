import requests
from django.conf import settings
from .models import Car


# By the way i decide to do it as the services inorder to fetch the external data provided
class CarAPIService:
    BASE_URL = "http://192.168.20.207:9191/api"

    @classmethod
    def fetch_cars(cls):
        """
     time to fetch cars from the external API and store them in the database
     now you taleked of if the service is down this is what i have for it
        """
        try:
            response = requests.get(f"{cls.BASE_URL}/cars/")
            response.raise_for_status()
            cars_data = response.json()
            
            for car_data in cars_data:
                car, created = Car.objects.update_or_create(
                    name=car_data['name'],
                    make=car_data['make'],
                    model=car_data['model'],
                    year=car_data['year'],
                    defaults={
                        'available': True,
                    }
                )
            
            return True, "Cars fetched and stored successfuly"
        except requests.RequestException as e:
            return False, f"Error fetching cars: {str(e)}"
        except Exception as e:
            return False, f"Error processing cars: {str(e)}"

    @classmethod
    def create_car(cls, car_data):
        """
        Create a new car through the external API
        """
        try:
            response = requests.post(
                f"{cls.BASE_URL}/cars/",
                json=car_data
            )
            response.raise_for_status()
            return True, response.json()
        except requests.RequestException as e:
            return False, f"Error creating car: {str(e)}"
        except Exception as e:
            return False, f"Error processing response: {str(e)}" 
from flask import *  
from kmeans import *
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AutoReg
from statsmodels.tsa.stattools import adfuller

from math import sqrt

from sklearn.metrics import mean_squared_error 

app = Flask(__name__) 
app.secret_key = "abc"  
haryana_district = ['Ambala','Bhiwani','Faridabad','Fatehabad','Grp','Gurugram','Hissar',
                     'Jhajjar','Jind','Kaithal','Karnal','Kurukshetra',
                    'Mahendergarh','Nuh','Palwal','Panchkula','Panipat',
                     'Rewari','Rohtak','Sirsa','Sonipat','Yamunanagar','Irrigation & Power',
                     'Charkhi Dadri','Hansi']

up_district = ["Agra","Aligarh","Prayagraj","Ambedkar Nagar","Amethi","Amroha"
        ,"Auraiya","Azamgarh","Badaun","Baghpat","Bahraich", "Ballia","Balrampur",
                "Banda","Barabanki","Bareilly","Basti","Bijnor","Bulandshahr","Chandoli",
                "Chitrakoot","Deoria","Etah","Etawah","Ayodhya","Fatehgarh","Fatehpur",
                "Firozabad","GRP","Gautambudh Nagar","Ghaziabad","Ghazipur","Gonda","Gorakhpur",
                "Hamirpur","Hapur","Hardoi","Hathras","Jalaun","Jaunpur","Jhansi","Kannauj","Kanpur Dehat",
                "Kanpur Nagar","Kasganj","Kaushambi","Khiri","Kushi Nagar","Lalitpur","Lucknow",
                "Maharajganj","Mahoba","Mainpuri","Mathura","Mau","Meerut","Mirzapur","Moradabad","Muzaffarnagar",
                "Pilibhit","Pratapgarh","Raibareilly", "Rampur","Saharanpur","Sambhal","Sant Kabirnagar","Shahjahanpur",
                "Shamli", "Shrawasti", "Sidharthnagar", "Sitapur", "Sonbhadra", "Bhadohi", "Sultanpur", "Unnao", "Varanasi"]


years2 = ["2021","2022","2023","2024","2025","2026"]
years1 = ["2013","2014","2015","2016","2017","2018","2019","2020"]
years3 = ["2015","2016","2017","2018","2019","2020"]
crimes = ['Murder','Robbery','Rape','Dowry','Accident','Kidnapping','Suicide']

@app.route('/',methods = ['POST', 'GET']) 
def home():
      return render_template("homepage.html")

@app.route('/kmean_cluster',methods = ['POST', 'GET'])  
def message():  
      if request.method == 'POST':  
            #FOR EXTRACTING DATA FROM WEBSITE
            year = request.form['year']  
            district = request.form['district'] 
            if(year != "" and district !=""):
                  num = (years1.index(year))
                  k = haryana_district.index(district.title())
                  r = num*25+k+1
                  with open('kmeans_haryana_dataset.csv', 'r') as csvfile:
                  # creating a csv reader object
                        csvreader = csv.reader(csvfile)
                        d = [row for idx, row in enumerate(csvreader) if idx == r][0]
                  total = 0
                  #DOING SUMMATION
                  for i in range(len(d)):
                        total = total + int(d[i])
                  j = k_means.predict([[total]])
                  j = int(str(j)[1:-1])

                  #ASSIGNING CATEGORY TO CLUSTER
                  f = rate.index(j)
                  # print(f)
                  area = rate_name[f]
                  show = True
                  return render_template("kmean_cluster.html",year = year , district = district,haryana_district=haryana_district,years = years1,area = area , show = show,crimes = crimes,d = d )
            else:
                  flash("Select all details")
                  return redirect(url_for('message')) 
      else:
            show = False
            return render_template('kmean_cluster.html',haryana_district=haryana_district,years = years1,show = show,crimes = crimes)  


@app.route('/kmean_cluster_up',methods = ['POST', 'GET'])  
def message_up():  
      if request.method == 'POST':  
            year = request.form['year']  
            district = request.form['district'] 
            if(year != "" and district !=""):
                  num = (years3.index(year))
                  k = up_district.index(district.title())
                  r = num*76+k+1
                  with open('kmeans_up_dataset.csv', 'r') as csvfile:
                  # creating a csv reader object
                        csvreader = csv.reader(csvfile)
                        d = [row for idx, row in enumerate(csvreader) if idx == r][0]
                  total = 0
                  for i in range(len(d)):
                        total = total + int(d[i])
                  j = k_means.predict([[total]])
                  j = int(str(j)[1:-1])

                  f = rate.index(j)
                  # print(f)
                  area = rate_name[f]
                  show = True
                  return render_template("kmean_cluster_up.html",year = year , district = district,up_district=up_district,years = years3,area = area , show = show,crimes = crimes,d = d )
            else:
                  flash("Select all details")
                  return redirect(url_for('message')) 
      else:
            show = False
            return render_template('kmean_cluster_up.html',up_district = up_district,years = years3,show = show,crimes = crimes) 


@app.route('/kmean_pred',methods = ['POST', 'GET'])
def kmean_pred():
      if request.method == 'POST':  
            murder = request.form['murder']  
            robbery = request.form['robbery']  
            rape = request.form['rape']  
            accident = request.form['accident']  
            kidnap = request.form['kidnap']  
            dowry = request.form['dowry']  
            suicide = request.form['suicide']  

            #DOING SUMMATION
            total = int(murder) + int(robbery) + int(rape) + int(dowry) + int(accident) + int(kidnap) + int(suicide)
            #ASSIGNING CLUSTER 
            j = k_means.predict([[total]])
            j = int(str(j)[1:-1])

            #ASSIGNING CATEGORY 
            f = rate.index(j)

            area = rate_name[f]
            show = True
            return render_template('kmean_pred.html',show = show,area = area,murder=murder,kidnap=kidnap,dowry=dowry,suicide=suicide,accident=accident,robbery=robbery,rape = rape)
      else:
            show = False
            return render_template('kmean_pred.html',show = show)

@app.route('/auto_reg',methods = ['POST', 'GET'])  
def prediction():  
      if request.method == 'POST':  
            year = request.form['year']  
            district = request.form['district'] 
            print(district)
            crime = request.form['crimes'] 
            print(crime)
            s = haryana_district.index(district.title())
            c = crimes.index(crime.title())    
            y = years2.index(year.title())    
            df=pd.read_csv('kmeans_haryana_dataset.csv', index_col=0, parse_dates=True)
            # print(type(df['Murder']))
            X=df.values
            # print(type(X))
            j = []

            X = list(X)

            f = s
            for i in range(7):
                  Y = X[f]
                  j.append(Y[c])
                  f = f + 25
            X = np.array(j)
            # dftest = adfuller (X, autolag = 'AIC')

            train=X
            model=AutoReg (train, lags=2).fit()
            # print(model.summary())
            pred=model.predict (start=2, end=len(X)+1, dynamic=False)

            rmse= sqrt(mean_squared_error(X, pred))
            rmspe = np.sqrt(np.mean(np.square(((X - pred) / X)), axis=0))

            print(rmspe)
            pred_future=model.predict(start=len(X)+1, end=len (X)+y+1, dynamic=False)

            p = round((list(pred_future)[-1]))
            show = True
            return render_template('auto_reg.html',haryana_district=haryana_district,years = years2,show = show,crimes=crimes,p = p,year = year,district = district,crime = crime)
      else:
            show = False
            return render_template('auto_reg.html',haryana_district=haryana_district,years = years2,show = show,crimes=crimes)

if __name__ == '__main__':   
   app.run(debug = True) 
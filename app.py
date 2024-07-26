import streamlit as st
import math

import pandas as pd
df=pd.read_csv(r'IPL_Ball_by_Ball_2008_2022.csv')
match=pd.read_csv(r'IPL_Matches_2008_2022.csv')
len(df)
match['Venue']=match['Venue'].str.replace('MA Chidambaram Stadium, Chepauk, Chennai','MA Chidambaram Stadium')
match['Venue']=match['Venue'].str.replace('Wankhede Stadium, Mumbai','Wankhede Stadium')

match['Venue']=match['Venue'].str.replace('Eden Gardens, Kolkata','Eden Gardens')

match['Venue']=match['Venue'].str.replace('Punjab Cricket Association IS Bindra Stadium, Mohali','Punjab Cricket Association Stadium, Mohali')
match['Venue']=match['Venue'].str.replace('Punjab Cricket Association IS Bindra Stadium','Punjab Cricket Association Stadium, Mohali')

match['Venue']=match['Venue'].str.replace('Arun Jaitley Stadium, Delhi','Arun Jaitley Stadium')
match['Venue']=match['Venue'].str.replace('Rajiv Gandhi International Stadium','Rajiv Gandhi International Stadium, Hyderabad')

match['Venue']=match['Venue'].str.replace('Rajiv Gandhi International Stadium, Hyderabad, Uppal','Rajiv Gandhi International Stadium, Hyderabad')


match['Venue']=match['Venue'].str.replace('M.Chinnaswamy Stadium','M Chinnaswamy Stadium')
match['Venue']=match['Venue'].str.replace('MA Chidambaram Stadium, Chepauk','MA Chidambaram Stadium')
match=match[match['method']!='D/L']
match=match[match['WonBy']!='NoResults']
merged_df = pd.merge(df,match, on='ID')

final= merged_df[['ID','Date','innings','overs','ballnumber','batter','bowler','non-striker','batsman_run','extras_run','BattingTeam','Team1','Team2','Season','Venue','Team1Players','Team2Players']]

import pandas as pd
df=pd.read_csv(r'IPL_Ball_by_Ball_2008_2022.csv')

final=final[final['innings']<3]

final['BattingTeam']=final['BattingTeam'].str.replace('Daredevils','Capitals')
final['BattingTeam']=final['BattingTeam'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
final['BattingTeam']=final['BattingTeam'].str.replace('Rising Pune Supergiants','Rising Pune Supergiant')
final['BattingTeam']=final['BattingTeam'].str.replace('Kings XI Punjab','Punjab Kings')

final['Team1']=final['Team1'].str.replace('Daredevils','Capitals')
final['Team1']=final['Team1'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
final['Team1']=final['Team1'].str.replace('Rising Pune Supergiants','Rising Pune Supergiant')
final['Team1']=final['Team1'].str.replace('Kings XI Punjab','Punjab Kings')

final['Team2']=final['Team2'].str.replace('Daredevils','Capitals')
final['Team2']=final['Team2'].str.replace('Deccan Chargers','Sunrisers Hyderabad')
final['Team2']=final['Team2'].str.replace('Rising Pune Supergiants','Rising Pune Supergiant')
final['Team2']=final['Team2'].str.replace('Kings XI Punjab','Punjab Kings')
df=final

df=df[df['BattingTeam']!='Pune Warriors']
df=df[df['BattingTeam']!='Gujarat Lions']
df=df[df['BattingTeam']!='Kochi Tuskers Kerala']
df=df[df['BattingTeam']!='Rising Pune Supergiant']

final=final[final['overs']<6]
df=df[df['overs']<6]

import numpy as np

piv=pd.pivot_table(df, values =['batsman_run','extras_run'],index=['ID','innings','BattingTeam','Team1','Team2','Venue','Season'],
                         aggfunc = np.sum)


piv['PP']=piv['extras_run']+piv['batsman_run']

piv.reset_index(level=0, inplace=True)
piv.reset_index(level=0, inplace=True)
piv.reset_index(level=0, inplace=True)
piv.reset_index(level=0, inplace=True)
piv.reset_index(level=0, inplace=True)
piv.reset_index(level=0, inplace=True)
piv.reset_index(level=0, inplace=True)
# Define your functions here
import math
def bowler_strikerate(batsman,bowler):
    h=final[final['batter']==batsman] 
    h=h[h['extras_run']==0]
    h=h[h['bowler']==bowler]
    if h['batsman_run'].sum()==0:
        return 1.35
    elif len(h)!=0:
        return h['batsman_run'].sum()/len(h)
    else:
        return 1.35

def stadium_strikerate(batsman,venue):
    h=final[final['batter']==batsman] 
    h=h[h['extras_run']==0]
    for i in final['Venue'].unique():
        if venue in i:
            venue=i
        
    h=h[h['Venue']==venue]
    if h['batsman_run'].sum()==0:
        return 1.35
    elif len(h)!=0:
        return h['batsman_run'].sum()/len(h)
    else:
        return 1.35

def innings_strikerate(batsman,innings):
    h=final[final['batter']==batsman] 
    h=h[h['extras_run']==0]
    h=h[h['innings']==innings]
    if h['batsman_run'].sum()==0:
        return 1.35
    elif len(h)!=0:
        return h['batsman_run'].sum()/len(h)
    else:
        return 1.35
    

batsmen=['V Kohli','F du Plessis']
bowlers=['TA Boult','R Ashwin','Avesh Khan']


def score(batsmen,bowlers,venue,innings,battingteam,bowlingteam):
    strike=[]
    for i in batsmen:
        s=0
        for j in bowlers:
            s+=bowler_strikerate(i,j)
        a=stadium_strikerate(i,venue)
        b=innings_strikerate(i,innings)
        s/=len(bowlers)
        strike.append((0.3*a)+(0.65*s)+(0.05*b))
    for i in range(len(strike)):
        strike[i]*=36/len(batsmen)
    bat=piv
    tem=bat[(bat['BattingTeam']==battingteam) & (bat['Season']=='2022')]['PP'].mean()
    res=((sum(strike)*0.65+tem*0.35))+piv[(piv['BattingTeam']!=bowlingteam) & ((piv['Team1']==bowlingteam) | (piv['Team2']==bowlingteam))]['extras_run'].mean()
    return math.ceil(0.6*res+0.4*piv[(piv['BattingTeam']!=bowlingteam) & ((piv['Team1']==bowlingteam) | (piv['Team2']==bowlingteam)) & (piv['Season']=='2022')]['PP'].mean())


# Define Streamlit app
def main():
    st.title('Cricket Score Predictor')

    # Input fields
    batsmen = st.multiselect('Select batsmen:', ['YBK Jaiswal', 'JC Buttler', 'SV Samson', 'WP Saha',
       'Shubman Gill', 'MS Wade', 'HH Pandya', 'V Kohli', 'F du Plessis',
       'RM Patidar', 'Q de Kock', 'KL Rahul', 'M Vohra', 'DJ Hooda',
       'PK Garg', 'Abhishek Sharma', 'RA Tripathi', 'JM Bairstow',
       'S Dhawan', 'M Shahrukh Khan', 'PP Shaw', 'DA Warner', 'MR Marsh',
       'RR Pant', 'SN Khan', 'Ishan Kishan', 'RG Sharma', 'D Brevis',
       'RD Gaikwad', 'DP Conway', 'MM Ali', 'VR Iyer', 'N Rana',
       'A Tomar', 'SS Iyer', 'Lalit Yadav', 'PBB Rajapaksa',
       'LS Livingstone', 'A Badoni', 'KH Pandya', 'AM Rahane',
       'KS Williamson', 'MK Lomror', 'GJ Maxwell', 'RV Uthappa',
       'AT Rayudu', 'MS Dhoni', 'S Dube', 'DR Sams', 'Tilak Varma',
       'T Stubbs', 'HR Shokeen', 'R Ashwin', 'KS Bharat', 'KS Sharma',
       'Ramandeep Singh', 'AK Markram', 'B Indrajith', 'AJ Finch',
       'RK Singh', 'Mandeep Singh', 'B Sai Sudharsan', 'D Padikkal',
       'SA Yadav', 'MA Agarwal', 'DJ Mitchell', 'MJ Santner', 'MK Pandey',
       'Anuj Rawat', 'SS Prabhudessai', 'Shahbaz Ahmed', 'SW Billings',
       'SP Narine', 'JM Sharma', 'V Shankar', 'A Manohar', 'DA Miller',
       'P Simran Singh', 'K Gowtham', 'JO Holder', 'E Lewis', 'RA Jadeja',
       'TL Seifert', 'Anmolpreet Singh', 'RA Bawa', 'SE Rutherford',
       'DJ Willey', 'N Pooran', 'MP Stoinis', 'AR Patel', 'SPD Smith',
       'JJ Roy', 'CH Gayle', 'GD Phillips', 'SK Raina', 'SS Tiwary',
       'AB de Villiers', 'EJG Morgan', 'DT Christian', 'DJ Malan',
       'Virat Singh', 'Washington Sundar', 'AD Russell', 'BA Stokes',
       'CA Lynn', 'SP Goswami', 'KD Karthik', 'T Banton', 'M Vijay',
       'SR Watson', 'SM Curran', 'R Parag', 'R Tewatia', 'N Jagadeesan',
       'SO Hetmyer', 'KM Jadhav', 'JR Philippe', 'KK Nair', 'C Munro',
       'MJ Guptill', 'PA Patel', 'Gurkeerat Singh', 'S Gopal', 'AD Nath',
       'JL Denly', 'SD Lad', 'NS Naik', 'CA Ingram', 'KA Pollard',
       'Shakib Al Hasan', 'MK Tiwary', 'Harbhajan Singh', 'JC Archer',
       'AD Hales', 'DJM Short', 'BB McCullum', 'JP Duminy', 'YK Pathan',
       'G Gambhir', 'RK Bhui', 'H Klaasen', 'Yuvraj Singh', 'LMP Simmons',
       'IR Jaggi', 'Vishnu Vinod', 'SE Marsh', 'DR Smith', 'MC Henriques',
       'HM Amla', 'TM Head', 'CJ Anderson', 'MN Samuels', 'PJ Cummins',
       'SP Jackson', 'STR Binny', 'AP Tare', 'K Rabada',
       'C de Grandhomme', 'MJ McClenaghan', 'ER Dwivedi', 'Sachin Baby',
       'NV Ojha', 'UT Khawaja', 'GJ Bailey', 'PP Chawla', 'UBT Chand',
       'KP Pietersen', 'P Negi', 'MEK Hussey', 'NJ Maddinson', 'V Sehwag',
       'GH Vihari', 'MS Bisla', 'RR Rossouw', 'DJ Bravo', 'CM Gautam',
       'JA Morkel', 'YV Takawale', 'VH Zol', 'DJ Hussey', 'KK Cooper',
       'Ankit Sharma', 'S Rana', 'BR Dunk', 'CA Pujara', 'JH Kallis',
       'AM Nayar', 'Y Venugopal Rao', 'LRPL Taylor', 'S Badrinath',
       'R Dravid', 'CL White', 'DPMD Jayawardene', 'B Chipli',
       'AC Gilchrist', 'Azhar Mahmood', 'BB Samantray', 'JP Faulkner',
       'J Botha', 'RN ten Doeschate', 'SR Tendulkar', 'RE van der Merwe',
       'LA Pomersbach', 'UA Birla', 'KC Sangakkara', 'PA Reddy',
       'A Ashish Reddy', 'TL Suman', 'LJ Wright', 'A Mukund',
       'TM Dilshan', 'KV Sharma', 'NLTC Perera', 'DJG Sammy', 'A Mishra',
       'IK Pathan', 'PC Valthaty', 'MC Juneja', 'BMAJ Mendis',
       'RT Ponting', 'S Anirudha', 'AD Mathews', 'MDKJ Perera',
       'JD Ryder', 'MJ Clarke', 'SD Chitnis', 'HH Gibbs', 'N Saini',
       'SC Ganguly', 'AP Majumdar', 'CJ Ferguson', 'Y Nagar', 'MD Mishra',
       'JEC Franklin', 'DJ Harris', 'RE Levi', 'AC Blizzard', 'OA Shah',
       'AL Menaria', 'DJ Jacobs', 'DB Das', 'AB McDonald', 'WD Parnell',
       'DB Ravi Teja', 'Y Gnaneswara Rao', 'S Sohal', 'FY Fazal',
       'BJ Hodge', 'MJ Lumb', 'A Symonds', 'M Klinger', 'JR Hopes',
       'Sunny Singh', 'GC Smith', 'AA Jhunjhunwala', 'TD Paine',
       'RV Gomez', 'M Manhas', 'VVS Laxman', 'BJ Haddin', 'R Sathish',
       'SA Asnodkar', 'AG Paunikar', 'AS Raut', 'AUK Pathan', 'Z Khan',
       'ML Hayden', 'Anirudh Singh', 'R McLaren', 'C Madan',
       'ST Jayasuriya', 'PD Collingwood', 'S Sriram', 'AB Barath',
       'AC Voges', 'RS Bopara', 'DR Martyn', 'JM Kemp', 'AA Bilakhia',
       'Mohammad Ashraful', 'SM Katich', 'RJ Quiney', 'NK Patel',
       'Yashpal Singh', 'AN Ghosh', 'LA Carseldine', 'MN van Wyk',
       'L Ronchi', 'PR Shah', 'W Jaffer', 'K Goel', 'R Bishnoi',
       'AD Mascarenhas', 'LR Shukla', 'P Kumar', 'A Chopra',
       'T Henderson', 'A Flintoff', 'S Vidyut', 'Kamran Akmal',
       'SB Styris', 'SP Fleming', 'Salman Butt', 'Mohammad Hafeez',
       'Sohail Tanvir', 'DJ Thornely', 'Shahid Afridi', 'LPC Silva',
       'J Arunkumar', 'Misbah-ul-Haq', 'M Kaif', 'Younis Khan',
       'RR Sarwan', 'MV Boucher', 'S Chanderpaul', 'AB Agarkar',
       'Shoaib Malik', 'SM Pollock', 'M Rawat', 'DS Lehmann', 'T Kohli'])
    bowlers = st.multiselect('Select bowlers:', ['Mohammed Shami', 'Yash Dayal', 'LH Ferguson', 'Rashid Khan',
       'TA Boult', 'M Prasidh Krishna', 'YS Chahal', 'Mohammed Siraj',
       'JR Hazlewood', 'GJ Maxwell', 'Shahbaz Ahmed', 'Mohsin Khan',
       'PVD Chameera', 'KH Pandya', 'Avesh Khan', 'AS Joseph', 'R Ashwin',
       'LS Livingstone', 'Arshdeep Singh', 'K Rabada', 'NT Ellis',
       'B Kumar', 'Washington Sundar', 'Fazalhaq Farooqi', 'J Suchith',
       'DR Sams', 'HR Shokeen', 'JJ Bumrah', 'KK Ahmed', 'A Nortje',
       'SN Thakur', 'MR Marsh', 'Mukesh Choudhary', 'Simarjeet Singh',
       'S Kaul', 'HH Pandya', 'UT Yadav', 'TG Southee', 'SP Narine',
       'CV Varun', 'JO Holder', 'K Gowtham', 'RP Meredith',
       'R Sanjay Yadav', 'T Natarajan', 'Harpreet Brar', 'R Dhawan',
       'Lalit Yadav', 'MJ Santner', 'M Jansen', 'AD Russell',
       'C Sakariya', 'AR Patel', 'M Ashwin', 'K Kartikeya', 'PJ Cummins',
       'M Theekshana', 'Kartik Tyagi', 'Shivam Mavi', 'AS Roy',
       'Harshit Rana', 'KR Sen', 'Sandeep Sharma', 'SA Abbott',
       'Umran Malik', 'PWH de Silva', 'PJ Sangwan', 'Mustafizur Rahman',
       'JD Unadkat', 'HV Patel', 'OC McCoy', 'VG Arora', 'CJ Jordan',
       'Tilak Varma', 'TS Mills', 'FA Allen', 'Ravi Bishnoi',
       'JDS Neesham', 'Basil Thampi', 'Akash Deep', 'MM Ali',
       'Rasikh Salam', 'DJ Willey', 'AJ Tye', 'R Shepherd', 'DJ Bravo',
       'Navdeep Saini', 'OF Smith', 'TU Deshpande', 'VR Aaron',
       'KL Nagarkoti', 'AF Milne', 'Shakib Al Hasan', 'DL Chahar',
       'GHS Garton', 'J Yadav', 'NM Coulter-Nile', 'IC Porel', 'DJ Hooda',
       'CH Morris', 'KA Jamieson', 'DT Christian', 'MK Lomror',
       'AK Markram', 'SM Curran', 'N Rana', 'S Gopal', 'K Yadav',
       'S Sandeep Warrier', 'Akash Singh', 'Mohammad Nabi', 'PP Chawla',
       'I Sharma', 'MP Stoinis', 'DS Kulkarni', 'L Ngidi', 'MC Henriques',
       'Abhishek Sharma', 'RD Chahar', 'KW Richardson', 'A Mishra',
       'CR Woakes', 'LI Meriwala', 'Jalaj S Saxena', 'JA Richardson',
       'Harbhajan Singh', 'Mujeeb Ur Rahman', 'S Nadeem', 'TK Curran',
       'JL Pattinson', 'I Udana', 'Monu Kumar', 'JC Archer', 'BA Stokes',
       'SS Cottrell', 'AS Rajpoot', 'V Shankar', 'DW Steyn', 'CJ Green',
       'Imran Tahir', 'MM Sharma', 'MJ McClenaghan', 'SL Malinga',
       'HF Gurney', 'O Thomas', 'IS Sodhi', 'BB Sran', 'S Lamichhane',
       'CR Brathwaite', 'Y Prithvi Raj', 'STR Binny', 'KC Cariappa',
       'GC Viljoen', 'KMA Paul', 'JP Behrendorff', 'RA Jadeja',
       'SC Kuggeleijn', 'LE Plunkett', 'B Laughlin', 'CJ Dala',
       'JPR Scantlebury-Searles', 'Ankit Sharma', 'MG Johnson', 'KM Asif',
       'SR Watson', 'JP Duminy', 'R Tewatia', 'Kuldeep Yadav', 'P Negi',
       'B Stanlake', 'A Dananjaya', 'K Khejroliya', 'BCJ Cutting',
       'R Vinay Kumar', 'KV Sharma', 'Z Khan', 'C de Grandhomme',
       'P Kumar', 'JP Faulkner', 'MJ Henry', 'DR Smith', 'A Choudhary',
       'S Badree', 'S Aravind', 'A Nehra', 'YK Pathan', 'IK Pathan',
       'Ankit Soni', 'SK Raina', 'Anureet Singh', 'CJ Anderson',
       'NB Singh', 'SS Agarwal', 'Bipul Sharma', 'MM Patel', 'SB Jakati',
       'AB Dinda', 'Iqbal Abdulla', 'Tejas Baroka', 'MS Gony',
       'S Kaushik', 'CH Gayle', 'M Morkel', 'KS Williamson',
       'NLTC Perera', 'KJ Abbott', 'M Vijay', 'PV Tambe', 'RP Singh',
       'Parvez Rasool', 'SM Boland', 'JA Morkel', 'P Sahu', 'JW Hastings',
       'GB Hogg', 'S Ladda', 'MA Starc', 'Azhar Mahmood', 'IC Pandey',
       'BE Hendricks', 'Gurkeerat Singh', 'D Wiese', 'J Botha',
       'M de Lange', 'AD Mathews', 'GS Sandhu', 'RG More', 'J Theron',
       'DJ Muthuswami', 'Karanveer Singh', 'AN Ahmed', 'P Suyal',
       'L Balaji', 'P Awana', 'PP Ojha', 'KK Cooper', 'R Rampaul',
       'VS Malik', 'WD Parnell', 'M Muralitharan', 'K Santokie',
       'BW Hilfenhaus', 'KA Pollard', 'DJG Sammy', 'R Shukla',
       'JH Kallis', 'M Kartik', 'SA Yadav', 'LR Shukla',
       'Y Venugopal Rao', 'Anand Rajan', 'AG Murtaza', 'RG Sharma',
       'BJ Hodge', 'MG Neser', 'AA Chavan', 'SMSM Senanayake',
       'Harmeet Singh', 'RE van der Merwe', 'A Mithun', 'BAW Mendis',
       'K Upadhyay', 'A Chandila', 'S Sreesanth', 'R McLaren', 'SW Tait',
       'AB Agarkar', 'GH Vihari', 'S Narwal', 'TL Suman', 'DJ Hussey',
       'B Lee', 'R Sharma', 'DP Nannes', 'BA Bhatt', 'AD Mascarenhas',
       'RJ Harris', 'AJ Finch', 'MN Samuels', 'JDP Oram', 'Sunny Gupta',
       'P Parameswaran', 'V Pratap Singh', 'TM Dilshan', 'TP Sudhindra',
       'AA Jhunjhunwala', 'AC Thomas', 'KP Appanna', 'Pankaj Singh',
       'S Dhawan', 'RR Powar', 'RJ Peterson', 'AB McDonald', 'A Singh',
       'DL Vettori', 'KMDN Kulasekara', 'CJ McKay', 'LJ Wright',
       'DE Bollinger', 'AL Menaria', 'A Ashish Reddy', 'KP Pietersen',
       'RR Bhatkal', 'JEC Franklin', 'DAJ Bracewell', 'SK Trivedi',
       'J Syed Mohammad', 'RW Price', 'JJ van der Wath', 'CK Langeveldt',
       'SJ Srivastava', 'ND Doshi', 'AM Salvi', 'SB Wagh', 'JE Taylor',
       'S Randiv', 'SK Warne', 'Kamran Khan', 'NL McCullum',
       'Joginder Sharma', 'NJ Rimmington', 'CRD Fernando', 'A Kumble',
       'A Symonds', 'SE Bond', 'SC Ganguly', 'WPUJC Vaas', 'S Tyagi',
       'VRV Singh', 'AC Voges', 'AP Dole', 'L Ablish', 'MF Maharoof',
       'R Bhatia', 'Jaskaran Singh', 'KAJ Roach', 'MB Parmar',
       'T Thushara', 'Y Nagar', 'YA Abdulla', 'A Uniyal', 'V Sehwag',
       'RA Shaikh', 'B Akhil', 'Mashrafe Mortaza', 'Shoaib Ahmed',
       'SS Sarkar', 'SM Harwood', 'LA Carseldine', 'D du Preez',
       'AM Nayar', 'FH Edwards', 'JD Ryder', 'GR Napier', 'RR Bose',
       'A Flintoff', 'Sohail Tanvir', 'M Ntini', 'GD McGrath',
       'Mohammad Asif', 'VY Mahesh', 'DP Vijaykumar', 'Shahid Afridi',
       'SM Pollock', 'Umar Gul', 'SB Styris', 'B Geeves', 'A Nel',
       'VS Yeligati', 'DNT Zoysa', 'RR Raje', 'Shoaib Akhtar',
       'PM Sarvesh Kumar', 'JR Hopes', 'Gagandeep Singh', 'SB Bangar',
       'ST Jayasuriya', 'SD Chitnis', 'P Amarnath', 'AA Noffke'])
    venue = st.selectbox('Enter venue:',['Narendra Modi Stadium, Ahmedabad', 'Eden Gardens',
       'Wankhede Stadium', 'Brabourne Stadium, Mumbai',
       'Dr DY Patil Sports Academy, Mumbai',
       'Maharashtra Cricket Association Stadium, Pune',
       'Dubai International Cricket Stadium', 'Sharjah Cricket Stadium',
       'Zayed Cricket Stadium, Abu Dhabi', 'Arun Jaitley Stadium',
       'MA Chidambaram Stadium', 'Sheikh Zayed Stadium',
       'Rajiv Gandhi International Stadium, Hyderabad',
       'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
       'Punjab Cricket Association Stadium, Mohali',
       'M Chinnaswamy Stadium', 'Sawai Mansingh Stadium',
       'Maharashtra Cricket Association Stadium',
       'Holkar Cricket Stadium', 'Feroz Shah Kotla', 'Green Park',
       'Saurashtra Cricket Association Stadium',
       'Shaheed Veer Narayan Singh International Stadium',
       'JSCA International Stadium Complex', 'Brabourne Stadium',
       'Sardar Patel Stadium, Motera', 'Barabati Stadium',
       'Subrata Roy Sahara Stadium',
       'Himachal Pradesh Cricket Association Stadium',
       'Dr DY Patil Sports Academy', 'Nehru Stadium',
       'Vidarbha Cricket Association Stadium, Jamtha',
       'New Wanderers Stadium', 'SuperSport Park', 'Kingsmead',
       'OUTsurance Oval', "St George's Park", 'De Beers Diamond Oval',
       'Buffalo Park', 'Newlands'])
    innings = st.selectbox('Select innings:', [1, 2])
    batting_team = st.selectbox('Enter batting team:', ['Rajasthan Royals', 'Royal Challengers Bangalore',
       'Sunrisers Hyderabad', 'Delhi Capitals', 'Chennai Super Kings',
       'Gujarat Titans', 'Lucknow Super Giants', 'Kolkata Knight Riders',
       'Punjab Kings', 'Mumbai Indians'])
    bowling_team = st.selectbox('Enter bowling team:', ['Rajasthan Royals', 'Royal Challengers Bangalore',
       'Sunrisers Hyderabad', 'Delhi Capitals', 'Chennai Super Kings',
       'Gujarat Titans', 'Lucknow Super Giants', 'Kolkata Knight Riders',
       'Punjab Kings', 'Mumbai Indians'])

    # Calculate score on button click
    if batsmen and bowlers and venue and innings and batting_team and bowling_team:
            if st.button('Calculate Score'):
                score_result = score(batsmen, bowlers, venue, innings, batting_team, bowling_team)
                st.success(f'Predicted score: {score_result}')
                st.image("kohli.jpeg", caption='Imman in my dm')
            else:
                st.warning("Please select all input fields before calculating the score.")

# Run the app
if __name__ == '__main__':
    main()

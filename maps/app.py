import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from streamlit_option_menu import option_menu
import joblib
train_model_forest = joblib.load('modelo_train.pkl')
from plotly.offline import iplot, init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)
import streamlit.components.v1 as components


# ---------------------SITE CONFIG----------------------#
st.set_page_config(
    page_title="Airbnb: Hawaii",
    page_icon="🌅",
    layout="centered")

with st.sidebar:
    selected = option_menu(
        menu_title = "Main Menu",
        options = ["Home","Informacion","Precio",'Avaliaciones',"Power Bi", 'Predictor de Precios'],
        icons = ["house","book",'coin','table',"bar-chart","calculator"],
        menu_icon = "cast",
        default_index = 0,)

# creando el contenido de las páginas de acuerdo a la opción seleccionada

# PAGE 1-------------------------------------
if selected == "Home":
    st.markdown("<h1 class='centered-text'>Análisis de datos del Airbnb Hawaii</h1>", unsafe_allow_html=True)
    st.markdown("<p class='justified-text'>Insideairbnb.com es un sitio web en el que se publican conjuntos de datos extraídos de la web de 'instantáneas' de ciudades. He descargado los archivos de Hawaii de la situación del 6 de diciembre de 2018.</p>", unsafe_allow_html=True)
    st.markdown("<p class='justified-text'>Pensé que era un conjunto de datos divertido para asumir. Además de la disputa de datos básicos y las tramas.</p>", unsafe_allow_html=True)
    st.markdown("<p class='justified-text'>También he agregado <strong>mapas interactivos de Folium, gráficos interactivos de tramas y extracción de texto de los comentarios de revisión.</strong></p>", unsafe_allow_html=True)
    st.image('https://imgur.com/qrVfcpS.png', use_column_width=True)
    st.image('https://imgur.com/TWlePLO.jpg', use_column_width=True)
    st.markdown("<p class='images-text'>imagenes: https://w0.peakpx.com/wallpaper/963/58/HD-wallpaper-hawaiian-waves-waves-nature-beaches-hawaii.jpg</p>", unsafe_allow_html=True)
    st.markdown("<p class='images-text'>imagenes: https://www.adonde-y-cuando.es/site/images/illustration/hawai_642.jpg </p>", unsafe_allow_html=True)

# PAGE 2-------------------------------------
if selected == "Informacion":

    st.markdown("<p class='subtitle'>Aquí puedes ver los diferentes alojamientos que se ofrecen y dónde están ubicados. Acércate en el mapa para ver más detalles:'</p>", unsafe_allow_html=True)
    with open("maps/map1.html", "r", encoding='utf-8') as f:     
        html_data = f.read()
        components.html(html_data, height=600)
    
    st.markdown("""
            ### Seleccione lo que mas le interese:              
        """)

    # ---------------------TABS (pestañas)----------------------#
    tab1, tab2, tab3 = st.tabs(
        ['Accomodations','Potencial Ilegales','Vulcanes']) 
    with tab1:
        
        ##  1. accommodations

        st.markdown('### Acomodaciones')
        
        st.write('Número de anuncios por vecindario')
        st.image('graficos/anuncios_por_vecindario.png', use_column_width=True)
   
        st.write('Cantidade de anuncios por dia')
        with open("graficos/listings_available_by_date.html", "r", encoding='utf-8') as f:     
            html_data = f.read()
        components.html(html_data, height=450)
   
        st.write('Tipos de Propriedads')
        st.image('graficos/tipos_propriedades_hawaii.png', use_column_width=True)

        st.write('Tipos de habitaciones')
        st.image('graficos/tipos_propriedades.png', use_column_width=True)

        st.write('Número de Alojados')
        st.image('graficos/acomodates.png', use_column_width=True)

    with tab2:
                
        ## 2. Government services

        private = pd.read_csv("csv_app/private.csv")
        host_private = pd.read_csv("csv_app/host_private.csv")

        st.markdown('### Analítica al servicio del gobierno')
        st.write('Hawaii tiene regulaciones diferentes de un condado a otro, y todas ellas están diseñadas para limitar el número de propiedades en alquiler. (https://www.hostaway.com/blog/airbnb-rules-in-hawaii/)')
            
        st.write('Encontrando Potenciales hoteles Ilegales')
        host_private
        
        st.write('Encontrando las cordenadas de los potenciales hoteles Ilegales')
        roompicks = private[private['host_id']== 468914400]
        roompicks = roompicks[['name','host_id', 'host_name', 'latitude', 'longitude']]
        roompicks.index.name = "listing_id"
        roompicks
        
        st.markdown('### Efectos no deseados de los anfitriones profesionales?')
        
        st.write('Cantidad de Anuncions por Anfitrión')
        freq = pd.read_csv("csv_app/freq.csv")
        host_prop = freq.groupby(['num_host_listings']).size().reset_index(name='count').transpose()
        host_prop.columns = host_prop.iloc[0]
        host_prop = host_prop.drop(host_prop.index[0])
        host_prop

        st.write('Algunos Anfitriones son claramente profesionales')
        freq = pd.read_csv("csv_app/freq2.csv")
        freq = freq.sort_values(by=['num_host_listings'], ascending=False)
        freq = freq[freq['num_host_listings'] >= 20]
        freq
    
    with tab3:
            
        # 4. Vulcanes
        st.markdown('### Vulcanes') 
        st.markdown("<p class='justified-text'>Mismo que poco probable que un volcán entre en erupción en Hawaii, es importante saber que la isla es un volcán en sí mismo.</p>", unsafe_allow_html=True)
        st.markdown("<p class='justified-text'>Hawaii es un archipiélago de islas volcánicas en el Océano Pacífico. Las islas son el resultado de la actividad volcánica que comenzó hace millones de años.</p>", unsafe_allow_html=True)
        st.markdown("<p class='justified-text'>La isla de Hawaii es el volcán más grande y activo del mundo.</p>", unsafe_allow_html=True)
        st.markdown("<p class='justified-text'>Es un volcán en escudo, lo que significa que es un volcán grande y de forma redondeada.</p>", unsafe_allow_html=True)
        st.image("https://static.temblor.net/wp-content/uploads/2018/05/hawaii-sp-7.jpg", use_column_width=True)


# PAGE 3----------------------------------
if selected == "Precio":
    st.markdown('### Precios')
    st.markdown('Abajo tenemos um mapa con el precio medio por vecindad, zoom para ver más detalles:')
    
    with open("maps/map3.html", "r", encoding='utf-8') as f:     
        html_data = f.read()
    components.html(html_data, height=450)

    st.markdown('Precio medio por dia para 2 personas')    
    with open("graficos/Average_Price_2_persons.html", "r", encoding='utf-8') as f:     
        html_data = f.read()
    components.html(html_data, height=450)
        
    st.markdown('Precio medio por vecindario')
    st.image('graficos/precio_medio_vecindario.png', use_column_width=True)
    with open("graficos/precio_vecindario.html", "r", encoding='utf-8') as f:     
        html_data = f.read()
    components.html(html_data, height=450)

    st.markdown('Precio medio por vecindario y tipo de habitación')
    with open("graficos/precio_habitacion_vecindario_box.html", "r", encoding='utf-8') as f:     
        html_data = f.read()
    components.html(html_data, height=450)
    st.image('graficos/precioxhabitacion_swarmplot.png', use_column_width=True)

# PAGE 3----------------------------------
if selected == "Avaliaciones":

    st.markdown("<p class='subtitles'>Puntaje Promedio de Revisión de Ubicación por Vecindario (con al menos 10 revisiones)</p>", unsafe_allow_html=True)
    st.image('graficos/review_score_price.png', use_column_width=True)
    
    st.markdown('Además de las reseñas escritas, los invitados pueden enviar una calificación de estrellas general y un conjunto de calificaciones de estrellas de categoría. Los huéspedes pueden dar calificaciones sobre:')
    st.markdown('* Experiencia general. ¿Cuál fue su experiencia en general?')
    st.markdown('* Limpieza. ¿Sentiste que tu espacio estaba limpio y ordenado?')
    st.markdown('* Precisión. ¿Con qué precisión su página de listado representó su espacio?')
    st.markdown('* Valor. ¿Sintió que su listado proporcionó un buen valor por el precio?')
    st.markdown('* Comunicación. ¿Qué tan bien se comunicó con su anfitrión antes y durante su estadía?')
    st.markdown('* Llegada. ¿Qué tan bien fue su registro?')
    st.markdown('* Ubicación. ¿Cómo te sentiste en el barrio?')
    st.markdown("<p class='subtitles'>A continuación puede ver la distribución de puntajes de todas esas categorías.'</p>", unsafe_allow_html=True)
    st.image('graficos/puntuaciones.png', use_column_width=True)

    st.markdown("<p class='subtitles'>A continuación, podemos ver que la parte más pequeña de los listados en Hawaii tienen un anfitrión que es Superanfitrión.</p>", unsafe_allow_html=True)
    st.image('graficos/list_superhost.png', use_column_width=True)   

    st.markdown("<p class='subtitles'>Palabras más comunes en los comentarios de los huéspedes em Hawaii:'</p>", unsafe_allow_html=True)
    st.image('graficos/wordcloud.png', use_column_width=True)


# PAGE 4----------------------------------
#if selected == "Power Bi":

# PAGE 5----------------------------------
if selected == "Predictor de Precios": 

    # Função para prever preço
    def predict_price(model, input_data):
        prediction = model.predict([input_data])
        return prediction[0]

    # Configurar o Streamlit
    st.title("Prevision de Preços Airbnb")
    st.write("Insira los datos para prever ell precio:")

    # Lista de vecindarios
    neighbourhoods = ['','Kauai', 'Honolulu', 'Maui', 'Hawaii']
    room_types = ['','Entire home/apt', 'Private room', 'Shared room', 'Hotel room']
    availability = ['','10','30','60','120','240','365']

    # Coletar entrada do usuário
    neighbourhood = st.selectbox("Vecindario", neighbourhoods)
    minimum_nights = st.number_input("Minimo de Notches permitida de la estancia", min_value=0)
    room_type = st.selectbox("Tipo de Habitacion", room_types)
    number_of_reviews = st.number_input("Numero de Reviews totales recibidos", min_value=0)
    reviews_per_month = st.number_input("Reviews recibidos por Mes", min_value=0)
    availability_365 = st.selectbox("Avaliable en el Año", availability)

    # Mapeamento de vecindarios para números
    neighbourhood_mapping = {name: idx for idx, name in enumerate(neighbourhoods)}
    neighbourhood_number = neighbourhood_mapping[neighbourhood]
    # Mapeamento de roomtype para números
    room_type_mapping = {name: idx for idx, name in enumerate(room_types)}
    room_type_number = room_type_mapping[room_type]

    # Preparar os dados de entrada
    input_data = [neighbourhood_number, room_type_number, minimum_nights, number_of_reviews, reviews_per_month, availability_365]

    # Prever o preço com base nos dados de entrada
    if st.button("Prever Precio"):
        predicted_price = predict_price(train_model_forest, input_data)
        st.write(f"El precio previsto es: ${predicted_price:.2f}")


# Adicionar CSS al app Streamlit
css = """
<style>
    [data-testid="stSidebar"] {
        background-image: url(https://imgur.com/6VyJtZt.png);
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }
    .header-black {
        color: black;
    }
        .centered-text {
        text-align: center;
        color: white;
        font-size: 40px;
        margin-bottom: 40px; 
    }
    .justified-text {
        text-align: justify;
        margin-bottom: 40px;
    }
    .images-text {
        font-size: 9px;
        color: grey;  
        margin-top: 00px;
    }
    .subtitles {
        font-size: 25px;
        color: White;  
        margin-top: 10px;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)
import axios from "axios";

axios.defaults.baseURL="https://proshop-dz.herokuapp.com"

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
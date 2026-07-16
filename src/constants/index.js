import {
  benefitIcon1,
  benefitIcon2,
  benefitIcon3,
  benefitIcon4,
  benefitImage2,
  discordBlack,
  facebook,
  file02,
  homeSmile,
  instagram,
  notification2,
  notification3,
  notification4,
  plusSquare,
  searchMd,
  telegram,
  twitter,
  yourlogo,
} from "../assets";

export const navigation = [
  {
    id: "0",
    title: "Why Aabar",
    url: "#features",
  },
  {
    id: "1",
    title: "Features",
    url: "#how-to-use",
  },
  {
    id: "2",
    title: "Roadmap",
    url: "#roadmap",
  },
  {
    id: "3",
    title: "Create account",
    url: "#signup",
    onlyMobile: true,
  },
  {
    id: "4",
    title: "Sign in",
    url: "#login",
    onlyMobile: true,
  },
];

export const heroIcons = [homeSmile, file02, searchMd, plusSquare];

export const notificationImages = [notification4, notification3, notification2];

export const companyLogos = [yourlogo, yourlogo, yourlogo, yourlogo, yourlogo];

export const aabarServices = [
  "pH",
  "Conductivity",
  "Temperature",
  "Depth evolution"
];

export const roadmap = [
  {
    id: "0",
    title: "Graph-based Radius Neighbors Regression",
    text: "TThe method used for water depth prediction can be described as a combination of radius-based regression and graph-based aggregation. In this approach, wells within a 5 km radius are selected as neighbors, akin to the traditional KNN method, where the proximity between wells determines their connection. Unlike traditional KNN, however, this method leverages a graph structure where edges represent the spatial distance between wells. The graph pre-encodes the spatial relationships, simplifying the process of identifying neighboring wells. To predict water depth, a weighted aggregation of the neighbors' values is performed, with closer wells (represented by shorter edges) contributing more to the prediction, similar to a weighted KNN regression. This technique effectively combines spatial statistics and graph-based learning.",
    date: "AabarPredict",
    status: "done",
    imageUrl: "./src/assets/gbrnr.png",
    colorful: true,
  },
  {
    id: "1",
    title: "Random Forest",
    text: "For coordinates where no neighboring wells exist, a Random Forest Regressor (RF) is used to predict water depth by leveraging various soil and weather characteristics. These characteristics, such as soil type, moisture content, temperature, and precipitation data, are obtained from the Google Earth Engine API, providing comprehensive environmental context for each location. The RF model, which is an ensemble learning method, takes these multiple input features and builds decision trees to predict the water depth at the given coordinates. By considering the interplay of soil and weather conditions, the Random Forest Regressor can make accurate predictions even in the absence of nearby well data, thus offering a robust solution for locations without direct spatial neighbors.",
    date: "AabarPredict",
    status: "progress",
    imageUrl: "./src/assets/rf.png",
  },
  {
    id: "2",
    title: "LLaMa",
    text: "Our LLM uses LLaMa since it's one of (if not the best) open source LLMs available and it supports multilingual queries and because no api inference model avaialable for pure darija / arabic query found during the dev of the MVP",
    date: "AnzarChat",
    status: "done",
    imageUrl: "./src/assets/llama.png",
  },
  {
    id: "3",
    title: "RAG",
    text: "To get relevant info, we use RAG to retrieve information from the water law number 36-15 therefore giving as accurate information as possible",
    date: "AnzarChat",
    status: "progress",
    imageUrl: "https://media1.tenor.com/m/bxYTfgCYDUYAAAAC/soul-terry.gif",
  },
];

export const benefits = [
  {
    id: "0",
    title: "90% of wells in Morocco are unauthorized",
    text: "According to official sources, 90% of wells in Morocco are unauthorized. This introduces a huge threat to the availability of groundwater.",
    backgroundUrl: "./src/assets/benefits/card-1.svg",
    iconUrl: benefitIcon1,
    imageUrl: benefitImage2,
  },
  {
    id: "1",
    title: "Tedious licensing process",
    text: "Licensing usually requires a lot of paperwork and tools to submit a demand to the responsible office, wasting time and money",
    backgroundUrl: "./src/assets/benefits/card-2.svg",
    iconUrl: benefitIcon2,
    imageUrl: benefitImage2,
    light: true,
  },
  {
    id: "2",
    title: "Expensive detection",
    text: "Detecting groundwater requires expensive (and we mean really expensive) equipments which can be a barrier for some people especially the farmers.",
    backgroundUrl: "./src/assets/benefits/card-3.svg",
    iconUrl: benefitIcon3,
    imageUrl: benefitImage2,
  },
  {
    id: "3",
    title: "Unclear laws",
    text: "Some people may not understand the laws regulating groundwater licensing and exploitation which may cause legal issues later on the process and cause a lot of losses.",
    backgroundUrl: "./src/assets/benefits/card-4.svg",
    iconUrl: benefitIcon4,
    imageUrl: benefitImage2,
    light: true,
  },
  {
    id: "4",
    title: "Lack of monitoring",
    text: "Most wells in Morocco are not monitored, which means that some wells can be contaminated which could present a major threat to the national health security.",
    backgroundUrl: "./src/assets/benefits/card-5.svg",
    iconUrl: benefitIcon1,
    imageUrl: benefitImage2,
  },
  {
    id: "5",
    title: "Lenghty process",
    text: "The process from paperwork to well digging can be very time-consuming taking weeks or even months which is a big issue especially that Morocco is facing water scarcity.",
    backgroundUrl: "./src/assets/benefits/card-6.svg",
    iconUrl: benefitIcon2,
    imageUrl: benefitImage2,
  },
];

export const socials = [
  {
    id: "0",
    title: "Discord",
    iconUrl: discordBlack,
    url: "#",
  },
  {
    id: "1",
    title: "Twitter",
    iconUrl: twitter,
    url: "#",
  },
  {
    id: "2",
    title: "Instagram",
    iconUrl: instagram,
    url: "#",
  },
  {
    id: "3",
    title: "Telegram",
    iconUrl: telegram,
    url: "#",
  },
  {
    id: "4",
    title: "Facebook",
    iconUrl: facebook,
    url: "#",
  },
];

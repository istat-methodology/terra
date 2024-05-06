import Vue from "vue"
import VueRouter from "vue-router"

import Error from "@/views/error/Error"
import Home from "@/views/Home"
import Maintenance from "@/views/Maintenance"

Vue.use(VueRouter)

//Vue.http.headers.common['Access-Control-Allow-Origin'] ="*";

let routes = [
  {
    path: "/error",
    component: Error,
    meta: {
      authorize: []
    }
  },
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      authorize: []
    }
  },
  {
    path: "/map",
    name: "Map",
    component: () => import("../views/map/Map"),
    meta: {
      authorize: []
    }
  },
  {
    path: "/privacy",
    name: "Privacy",
    component: () => import("../views/privacy/Privacy"),
    meta: {
      authorize: []
    }
  },
  {
    path: "/graphextra",
    name: "GraphExtraUe",
    props: { isIntra: false },
    component: () => import("../views/graph/Graph"),
    meta: {
      authorize: []
    }
  },
  {
    path: "/graphintra",
    name: "GraphIntraUe",
    props: { isIntra: true },
    component: () => import("../views/graph/Graph"),
    meta: {
      authorize: []
    }
  },
  {
    path: "/timeseries",
    name: "TimeSeries",
    component: () => import("../views/timeseries/TimeSeries"),
    meta: {
      authorize: []
    }
  },
  {
    path: "/trade",
    name: "Trade",
    component: () => import("../views/trade/Trade"),
    meta: {
      authorize: []
    }
  },
  {
    path: "/news",
    name: "News",
    component: () => import("../views/news/News"),
    meta: {
      authorize: []
    }
  },
  {
    path: "*",
    redirect: "/"
  }
]

if (window.Maintenance) {
  routes[1] = {
    path: "/",
    name: "Maintenance",
    component: Maintenance,
    meta: {
      authorize: []
    }
  }
}

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
})

export default router

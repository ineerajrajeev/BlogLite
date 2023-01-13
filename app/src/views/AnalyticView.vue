<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font overflow-hidden">
      <div class="container px-5 py-24 mx-auto">
        <div class="flex flex-wrap -m-12">
          <div class="flex flex-col text-center w-full mb-20">
            <h2
              class="text-xs text-indigo-500 tracking-widest font-medium title-font mb-1"
            >
              Graphical report
            </h2>
            <h1
              class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900"
            >
              Analytics
            </h1>
            <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
              Get graphical report for your activities and Interactions with
              your posts by your followers.
            </p>
            <p class="mx-auto leading-relaxed text-base">
              <a class="button-77" @click.prevent="downloadPdf">
                <i class="bx bxs-file-pdf"></i> Monthly report
              </a>
              .
              <a class="button-99" @click.prevent="downloadHtml">
                <i class="bx bxl-html5"></i> Monthly report
              </a>
            </p>
          </div>
          <div class="p-12 md:w-1/2 flex flex-col items-start">
            <span
              class="inline-block py-1 px-2 rounded bg-indigo-50 text-indigo-500 text-xs font-medium tracking-widest"
              >Likes</span
            >
            <h2
              class="sm:text-3xl text-2xl title-font font-medium text-gray-900 mt-4 mb-4"
            >
              Likes to your posts
            </h2>
            <p class="leading-relaxed mb-8">
              <canvas id="likes_chart" width="600" height="500"></canvas>
            </p>
          </div>
          <div class="p-12 md:w-1/2 flex flex-col items-start">
            <span
              class="inline-block py-1 px-2 rounded bg-indigo-50 text-indigo-500 text-xs font-medium tracking-widest"
              >No. of Posts</span
            >
            <h2
              class="sm:text-3xl text-2xl title-font font-medium text-gray-900 mt-4 mb-4"
            >
              Posts by you over year
            </h2>
            <p class="leading-relaxed mb-8">
              <canvas id="posts_over year" width="600" height="500"></canvas>
            </p>
          </div>
        </div>
      </div>
    </section>
  </section>
</template>

<script>
import NavBar from "../components/NavBar.vue";
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  name: "AnalyticView",
  beforeCreate: function () {
    const token = localStorage.getItem("blog_lite_token");
    fetch("http://127.0.0.1:5000/api/verify_token", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status != "success") {
          this.$router.push("/");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  components: {
    NavBar,
  },
  mounted: async function () {
    const token = localStorage.getItem("blog_lite_token");
    const data = await axios
      .get("http://127.0.0.1:5000/api/analytics", {
        headers: {
          "Content-Type": "application/json",
          "x-access-token": token,
        },
      })
      .then((res) => res.data);
    const ctx = document.getElementById("likes_chart");
    const myChart = new Chart(ctx, {
      data: {
        labels: data.likes_data.titles,
        datasets: [
          {
            type: "bar",
            label: "Likes",
            data: data.likes_data.likes,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
          {
            type: "line",
            label: "Likes",
            data: data.likes_data.likes,
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
    myChart.render();
    const ctx2 = document.getElementById("posts_over year");
    const myChart2 = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: data.months,
        datasets: [
          {
            label: "Posts",
            data: data.posts_over_last_month,
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(54, 162, 235, 0.2)",
              "rgba(255, 206, 86, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
              "rgba(255, 159, 64, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(54, 162, 235, 1)",
              "rgba(255, 206, 86, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
              "rgba(255, 159, 64, 1)",
            ],
            borderWidth: 1,
          },
          {
            type: "line",
            label: "Posts",
            data: data.posts_over_last_month,
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
    myChart2.render();
  },
  methods: {
    downloadPdf() {
      const url = "http://127.0.0.1:5000/api/pdf_report";
      const token = localStorage.getItem("blog_lite_token");
      axios({
        url: url,
        method: "GET",
        responseType: "blob", // important
        headers: {
          "x-access-token": token,
        },
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "report.pdf");
        document.body.appendChild(link);
        link.click();
      });
    },
    downloadHtml() {
      const url = "http://127.0.0.1:5000/api/html_report";
      const token = localStorage.getItem("blog_lite_token");
      axios({
        url: url,
        method: "GET",
        responseType: "blob", // important
        headers: {
          "x-access-token": token,
        },
      }).then((response) => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "report.html");
        document.body.appendChild(link);
        link.click();
      });
    },
  },
};
</script>

<style>
.home-section {
  position: relative;
  background: #e4e9f7;
  min-height: 100vh;
  top: 0;
  left: 78px;
  width: calc(100% - 78px);
  transition: all 0.5s ease;
  z-index: 2;
}
.sidebar.open ~ .home-section {
  left: 250px;
  width: calc(100% - 250px);
}
.home-section .text {
  display: inline-block;
  color: #11101d;
  font-size: 25px;
  font-weight: 500;
  margin: 18px;
}
.button-77 {
  background-color: #fbc2c2;
  border-radius: 100px;
  box-shadow: rgba(187, 44, 44, 0.2) 0 -25px 18px -14px inset,
    rgba(187, 44, 44, 0.15) 0 1px 2px, rgba(187, 44, 44, 0.15) 0 2px 4px,
    rgba(187, 44, 44, 0.15) 0 4px 8px, rgba(187, 44, 44, 0.15) 0 8px 16px,
    rgba(187, 44, 44, 0.15) 0 16px 32px;
  color: rgb(128, 0, 0);
  cursor: pointer;
  display: inline-block;
  font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;
  padding: 7px 20px;
  text-align: center;
  text-decoration: none;
  transition: all 250ms;
  border: 0;
  font-size: 16px;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}
.button-77:hover {
  box-shadow: rgba(187, 44, 44, 0.35) 0 -25px 18px -14px inset,
    rgba(187, 44, 44, 0.25) 0 1px 2px, rgba(187, 44, 44, 0.25) 0 2px 4px,
    rgba(187, 44, 44, 0.25) 0 4px 8px, rgba(187, 44, 44, 0.25) 0 8px 16px,
    rgba(187, 44, 44, 0.25) 0 16px 32px;
  transform: scale(1.05) rotate(-1deg);
}
.button-99 {
  background-color: #c2c9fb;
  border-radius: 100px;
  box-shadow: rgba(44, 61, 187, 0.2) 0 -25px 18px -14px inset,
    rgba(44, 61, 187, 0.15) 0 1px 2px, rgba(44, 61, 187, 0.15) 0 2px 4px,
    rgba(44, 61, 187, 0.15) 0 4px 8px, rgba(44, 61, 187, 0.15) 0 8px 16px,
    rgba(44, 61, 187, 0.15) 0 16px 32px;
  color: rgb(0, 21, 128);
  cursor: pointer;
  display: inline-block;
  font-family: CerebriSans-Regular, -apple-system, system-ui, Roboto, sans-serif;
  padding: 7px 20px;
  text-align: center;
  text-decoration: none;
  transition: all 250ms;
  border: 0;
  font-size: 16px;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}
.button-99:hover {
  box-shadow: rgba(44, 58, 187, 0.35) 0 -25px 18px -14px inset,
    rgba(44, 63, 187, 0.25) 0 1px 2px, rgba(44, 63, 187, 0.25) 0 2px 4px,
    rgba(44, 63, 187, 0.25) 0 4px 8px, rgba(44, 63, 187, 0.25) 0 8px 16px,
    rgba(44, 63, 187, 0.25) 0 16px 32px;
  transform: scale(1.05) rotate(-1deg);
}
</style>

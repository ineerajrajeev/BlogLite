<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font relative">
      <div class="container px-5 py-24 mx-auto">
        <div class="flex flex-col text-center w-full mb-12">
          <h1
            class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900"
          >
            Edit blog : {{ post.title }}
          </h1>
        </div>
        <div class="lg:w-2/3 md:w-2/3 mx-auto">
          <div class="flex flex-wrap -m-2">
            <div class="p-2 w-full">
              <div class="relative">
                <label for="title" class="leading-7 text-sm text-gray-600"
                  >Title</label
                >
                <input
                  type="text"
                  id="title"
                  name="title"
                  v-model="post.title"
                  class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                  required
                />
              </div>
            </div>
            <div class="p-2 w-full">
              <div class="relative">
                <label for="email" class="leading-7 text-sm text-gray-600"
                  >Caption</label
                >
                <input
                  type="text"
                  id="caption"
                  name="caption"
                  v-model="post.caption"
                  class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                  required
                />
              </div>
            </div>
            <div class="p-2 w-full">
              <div class="relative">
                <label for="message" class="leading-7 text-sm text-gray-600"
                  >Content</label
                >
                <textarea
                  id="message"
                  name="message"
                  v-model="post.content"
                  class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 h-40 text-base outline-none text-gray-700 py-1 px-3 resize-none leading-6 transition-colors duration-200 ease-in-out"
                  required
                ></textarea>
              </div>
            </div>
            <div class="p-2 w-full">
              <button
                @click="edit_blog()"
                class="flex mx-auto text-white bg-indigo-500 border-0 py-2 px-8 focus:outline-none hover:bg-indigo-600 rounded text-lg"
              >
                Post
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </section>
</template>

<script>
import NavBar from "../components/NavBar.vue";

export default {
  name: "AnalyticView",
  beforeCreate: function () {
    const token = localStorage.getItem("blog_lite_token");
    // make an api call to check if the token is valid
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

    fetch("http://127.0.0.1:5000/api/fetch_blog/" + this.$route.params.id, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "success") {
          this.post.title = data.message.blog.title;
          this.post.content = data.message.blog.description;
          this.post.caption = data.message.blog.caption;
          this.post.author = data.message.author;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  data() {
    return {
      post: {
        title: "",
        content: "",
        caption: "",
      },
    };
  },
  components: {
    NavBar,
  },
  methods: {
    edit_blog() {
      // const token = localStorage.getItem("blog_lite_token");
      const form = {
        title: this.post.title,
        description: this.post.content,
        caption: this.post.caption,
        blog_id: this.$route.params.id,
      };
      fetch("http://127.0.0.1:5000/api/edit_blog", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
        body: JSON.stringify(form),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status == "success") {
            this.$router.push("/dashboard");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
      console.log(form);
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
</style>

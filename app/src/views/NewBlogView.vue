<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font relative">
      <div class="container px-5 py-24 mx-auto">
        <div class="flex flex-col text-center w-full mb-12">
          <h1
            class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900"
          >
            New Blog
          </h1>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
            Create new blog to share your thoughts with your followers
          </p>
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
            <div class="p-2 w-2/5">
              <div class="relative">
                <label for="image" class="leading-7 text-sm text-gray-600"
                  >Image</label
                >
                <input
                  type="file"
                  id="title"
                  name="title"
                  @change="onFileSelected"
                  class="w-full bg-gray-100 bg-opacity-50 rounded border border-gray-300 focus:border-indigo-500 focus:bg-white focus:ring-2 focus:ring-indigo-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
                />
              </div>
            </div>
            <div class="p-2 w-2/5">
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
            <div class="p-2 w-1/5">
              <label for="caption" class="leading-7 text-sm text-gray-600"
                >Visibility </label
              ><br />
              <label class="switch">
                <input type="checkbox" v-model="post.visibility" />
                <span class="slider round"></span>
              </label>
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
                @click="new_blog"
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
  name: "NewBlogView",
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
  },
  components: {
    NavBar,
  },
  data() {
    return {
      post: {
        title: "",
        content: "",
        image: "",
        caption: "",
        visibility: false,
      },
    };
  },
  methods: {
    onFileSelected(event) {
      this.post.image = event.target.files[0];
    },
    new_blog() {
      const token = localStorage.getItem("blog_lite_token");
      if (this.post.title == "" || this.post.content == "") {
        alert("Please fill all the fields");
        return;
      }
      const formData = new FormData();
      formData.append("title", this.post.title);
      formData.append("description", this.post.content);
      formData.append("img", this.post.image);
      formData.append("caption", this.post.caption);
      formData.append("state", this.post.visibility);
      fetch("http://127.0.0.1:5000/api/new_blog", {
        method: "POST",
        headers: {
          "x-access-token": token,
        },
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status == "success") {
            this.$router.push("/profile");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
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
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

/* Hide default HTML checkbox */
.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

/* The slider */
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: 0.4s;
  transition: 0.4s;
}

input:checked + .slider {
  background-color: #2196f3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196f3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>

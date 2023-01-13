<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font">
      <div class="container px-3 py-15 mx-auto flex flex-col">
        <div class="lg:w-5/6 mx-auto">
          <div class="text-center mb-20 container px-5 py-12 mx-auto">
            <h1
              class="sm:text-3xl text-2xl font-medium title-font text-gray-900 mb-4"
            >
              Feed
            </h1>
            <div class="flex mt-6 justify-center">
              <div
                class="w-16 h-1 rounded-full bg-indigo-500 inline-flex"
              ></div>
            </div>
          </div>
          <div class="flex flex-col sm:flex-row mt-10">
            <div class="sm:w-6/7 text-center sm:pr-8 sm:py-8">
              <div class="container px-5 mx-auto flex flex-col bg-gray-100">
                <div class="mx-auto" v-if="blogs.length > 0">
                  <div
                    class="flex flex-col sm:flex-row sm:mt-0 py-10 w-full"
                    v-for="blog in blogs"
                    :key="blog.id"
                  >
                    <div class="container px-5 py-24 mx-auto">
                      <div class="mx-auto flex flex-wrap">
                        <div
                          class="lg:w-1/2 w-full lg:pr-10 lg:py-6 mb-6 lg:mb-0"
                        >
                          <h2
                            class="text-sm title-font text-gray-500 tracking-widest"
                          >
                            {{ blog.blog.date_created }}
                          </h2>
                          <h1
                            class="text-gray-900 text-3xl title-font font-medium mb-4"
                          >
                            {{ blog.blog.title }}
                          </h1>
                          <h2
                            class="text-sm title-font text-gray-500 tracking-widest"
                          >
                            {{ blog.author.name }} {{ blog.author.surname }} |
                            <a
                              :href="'/user/' + blog.author.username"
                              class="text-sm title-font text-gray-500 tracking-widest"
                            >
                              @{{ blog.author.username }}
                            </a>
                          </h2>
                          <h2
                            class="text-sm title-font text-gray-500 tracking-widest"
                          >
                            Likes: {{ blog.blog.likes }}
                          </h2>
                          <button
                            class="button-77"
                            @click="
                              like_post(blog.blog.blog_id);
                              blog.liked = !blog.liked;
                              blog.blog.likes += blog.liked ? 1 : -1;
                            "
                          >
                            <span v-if="blog.liked"
                              ><i class="bx bxs-like"></i
                            ></span>
                            <span v-else><i class="bx bx-like"></i></span>
                          </button>
                          .
                          <a
                            class="button-44"
                            alt="export"
                            :href="
                              'http://127.0.0.1:5000/api/export_html/' +
                              blog.blog.blog_id
                            "
                          >
                            <i class="bx bx-export"></i>
                          </a>
                          <br />
                          <div class="flex border-t border-gray-200 py-2">
                            {{ blog.blog.description }}
                          </div>
                        </div>
                        <img
                          :alt="blog.blog.caption"
                          class="lg:w-1/2 w-full lg:h-auto h-40 object-cover object-center rounded"
                          :src="blog_image(blog.blog.blog_id)"
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div class="mx-auto" v-else>
                  <div
                    class="flex flex-col sm:flex-row mt-10 sm:mt-0 py-10 text-center"
                  >
                    <span class="leading-relaxed text-lg">
                      There are no posts in your feed
                      <br />
                      Connect with others to see what they are posting
                    </span>
                  </div>
                </div>
              </div>
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
  name: "HomeView",
  beforeCreate: async function () {
    const token = localStorage.getItem("blog_lite_token");
    // make an api call to check if the token is valid
    await fetch("http://127.0.0.1:5000/api/verify_token", {
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

    // Fetch feed
    await fetch("http://127.0.0.1:5000/api/fetch_posts", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "success") {
          this.blogs = data.message;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  data() {
    return {
      blogs: [],
    };
  },
  methods: {
    blog_image(blog_id) {
      return "http://127.0.0.1:5000/api/blog_image/" + blog_id;
    },
    like_post(blog_id) {
      fetch("http://127.0.0.1:5000/api/like", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
        body: JSON.stringify({
          blog_id: blog_id,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status == "success") {
            return null;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
  },
  components: {
    NavBar,
  },
  computed: {
    blogImage(blog_id) {
      return "https://127.0.0.1:5000/api/blog_image/" + blog_id;
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

.button-44 {
  background-color: #fbf8c2;
  border-radius: 100px;
  box-shadow: rgba(187, 187, 44, 0.2) 0 -25px 18px -14px inset,
    rgba(187, 187, 44, 0.2) 0 1px 2px, rgba(187, 187, 44, 0.2) 0 2px 4px,
    rgba(187, 187, 44, 0.2) 0 4px 8px, rgba(187, 187, 44, 0.2) 0 8px 16px,
    rgba(187, 187, 44, 0.2) 0 16px 32px;
  color: rgb(126, 128, 0);
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

.button-44:hover {
  box-shadow: rgba(187, 187, 44, 0.35) 0 -25px 18px -14px inset,
    rgba(187, 187, 44, 0.35) 0 1px 2px, rgba(187, 187, 44, 0.35) 0 2px 4px,
    rgba(187, 187, 44, 0.35) 0 4px 8px, rgba(187, 187, 44, 0.35) 0 8px 16px,
    rgba(187, 187, 44, 0.35) 0 16px 32px;
  transform: scale(1.05) rotate(-1deg);
}
</style>

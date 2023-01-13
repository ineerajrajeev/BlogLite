<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font">
      <div class="container py-20 mx-auto flex flex-col">
        <div class="lg:w-5/6 mx-auto">
          <div class="flex flex-col sm:flex-row mt-10">
            <div class="sm:w-1/3 text-center sm:pr-8 sm:py-8 rounded-lg">
              <div
                class="flex flex-wrap w-full mb-10 flex-col items-center text-center"
              >
                <h1
                  class="sm:text-3xl text-2xl font-medium title-font text-gray-900"
                >
                  Profile
                </h1>
              </div>
              <div
                class="w-20 h-20 rounded-full inline-flex items-center justify-center text-gray-400"
                style="border-radius: 50%"
              >
                <img
                  class="w-20 h-20 rounded-full inline-flex items-center justify-center bg-gray-200 text-gray-400"
                  style="border-radius: 50%"
                  :src="getProfilePic"
                />
              </div>
              <div
                class="flex flex-col items-center text-center justify-center"
              >
                <h1 class="font-medium title-font mt-4 text-gray-900 text-lg">
                  <strong>{{ user.name }} {{ user.surname }}</strong>
                </h1>
                <div class="w-12 h-1 rounded mt-2 mb-4"></div>
                <p class="text-base">
                  <strong>Posts: </strong>{{ blogs.length }} |
                  <a href="/followers"
                    ><strong>Following: </strong>{{ user.following }}</a
                  >
                  |
                  <a href="/followers"
                    ><strong>Followers: </strong>{{ user.followers }}</a
                  >
                </p>
                <div class="w-12 h-1 bg-indigo-500 rounded mt-2 mb-4"></div>
                <strong class="text-base" v-if="user.bio != null">
                  {{ user.bio }}
                </strong>
                <span class="text-base" v-if="user.website != null">
                  <strong>Website: </strong>
                  <a v-bind:href="user.website">
                    {{ user.website }}
                  </a>
                </span>
                <span class="text-base">
                  <strong>Email ID: </strong>
                  <a v-bind:href="emailLink">
                    {{ user.email }}
                  </a>
                </span>
              </div>
            </div>
            <div
              class="sm:w-2/3 sm:pl-8 sm:py-8 sm:border-l border-gray-200 sm:border-t-0 border-t mt-4 pt-4 sm:mt-0 text-center sm:text-left"
            >
              <div
                class="flex flex-wrap w-full mb-10 flex-col items-center text-center"
              >
                <h1
                  class="sm:text-3xl text-2xl font-medium title-font text-gray-900"
                >
                  Your blogs
                </h1>
              </div>
              <div class="leading-relaxed text-lg mb-4">
                <div class="container px-5 mx-auto flex flex-col bg-gray-100">
                  <div class="mx-auto" v-if="blogs.length > 0">
                    <div
                      class="flex flex-col sm:flex-row mt-10 sm:mt-0 py-10"
                      v-for="blog in blogs"
                      :key="blog.id"
                    >
                      <div class="sm:w-1/4 text-center sm:pr-8 sm:py-8">
                        <div
                          class="flex flex-col items-center text-center justify-center"
                        >
                          <img
                            alt="blog"
                            :src="
                              'http://127.0.0.1:5000/api/blog_image/' +
                              blog.blog.blog_id
                            "
                          />
                          <h2
                            class="font-medium title-font mt-4 text-gray-900 text-lg"
                          >
                            {{ blog.author.name }}
                            {{ blog.author.surname }}
                          </h2>
                          <div
                            class="w-12 h-1 bg-indigo-500 rounded mt-2 mb-4"
                          ></div>
                          <p class="text-base">
                            {{ blog.author.username }}
                          </p>
                        </div>
                      </div>
                      <div
                        class="sm:w-3/4 sm:pl-8 sm:py-8 sm:border-l border-gray-200 sm:border-t-0 border-t mt-4 pt-4 sm:mt-0 text-center sm:text-left"
                      >
                        <p class="leading-relaxed text-lg">
                          <strong>{{ blog.blog.title }}</strong>
                        </p>
                        <p class="text-xs text-gray-500">
                          {{ blog.blog.date_created }}
                        </p>
                        <p class="text-xs text-gray-500">
                          Likes: {{ blog.blog.likes }}
                        </p>
                        <span class="text-base">
                          <button
                            class="button-77"
                            role="button"
                            @click="deleteBlog(blog.blog.blog_id)"
                          >
                            <i class="bx bxs-trash"></i>
                          </button>
                          .
                          <button
                            class="button-11"
                            role="button"
                            @click="
                              hideBlog(blog.blog.blog_id);
                              blog.blog.state = !blog.blog.state;
                            "
                            v-html="blogState(blog.blog.state)"
                          ></button>
                          .
                          <a
                            class="button-44"
                            role="button"
                            target="_blank"
                            :href="'/editBlog/' + blog.blog.blog_id"
                            ><i class="bx bx-edit-alt"></i>
                          </a>
                        </span>
                        <p class="leading-relaxed text-lg mb-4 mt-3">
                          {{ blog.blog.description }}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div class="mx-auto" v-else>
                    <div class="flex flex-col sm:flex-row mt-10 sm:mt-0 py-10">
                      <div class="sm:w-1/4 text-center sm:pr-8 sm:py-8">
                        <div
                          class="flex flex-col items-center text-center justify-center"
                        >
                          <h2
                            class="font-medium title-font mt-4 text-gray-900 text-lg"
                          >
                            No blogs
                          </h2>
                          <div
                            class="w-12 h-1 bg-indigo-500 rounded mt-2 mb-4"
                          ></div>
                          <p class="text-base">
                            You have not created any blogs yet.
                          </p>
                        </div>
                      </div>
                      <div
                        class="sm:w-3/4 sm:pl-8 sm:py-8 sm:border-l border-gray-200 sm:border-t-0 border-t mt-4 pt-4 sm:mt-0 text-center sm:text-left"
                      >
                        <p class="leading-relaxed text-lg">
                          <strong>Start creating blogs</strong>
                        </p>
                        <p class="text-xs text-gray-500">
                          Click on the button below to create a new blog.
                        </p>
                        <span class="text-base">
                          <a
                            class="button-77"
                            role="button"
                            @click="$router.push('/newBlog')"
                          >
                            Create Blog
                          </a>
                        </span>
                      </div>
                    </div>
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
  name: "ProfileView",
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

    fetch("http://127.0.0.1:5000/api/profile", {
      method: "GET",
      headers: {
        "Content-Type": "application",
        "x-access-token": localStorage.getItem("blog_lite_token"),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        this.user = data.user;
      });

    fetch("http://127.0.0.1:5000/api/fetch_profile_posts", {
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
  components: {
    NavBar,
  },
  data() {
    return {
      user: {},
      blogs: [],
    };
  },
  computed: {
    getProfilePic() {
      const img_url =
        "http://localhost:5000/api/profile_pic/" + this.user.username;
      return img_url;
    },
    emailLink() {
      const email = "mailto:" + this.user.email;
      return email;
    },
  },
  methods: {
    blogState(state) {
      if (state) {
        return "<i class='bx bx-low-vision' ></i>";
      } else {
        return "<i class='bx bx-color'></i>";
      }
    },
    deleteBlog(blog_id) {
      fetch("http://127.0.0.1:5000/api/delete", {
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
            alert(data["message"]);
            this.$router.go();
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },
    hideBlog(blog_id) {
      fetch("http://127.0.0.1:5000/api/hide", {
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
            alert(data.message);
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

.button-11 {
  background-color: #fbc2fa;
  border-radius: 100px;
  box-shadow: rgba(187, 44, 187, 0.2) 0 -25px 18px -14px inset,
    rgba(187, 44, 187, 0.15) 0 1px 2px, rgba(187, 44, 187, 0.15) 0 2px 4px,
    rgba(187, 44, 187, 0.15) 0 4px 8px, rgba(187, 44, 187, 0.15) 0 8px 16px,
    rgba(187, 44, 187, 0.15) 0 16px 32px;
  color: rgb(128, 0, 126);
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

.button-11:hover {
  box-shadow: rgba(187, 44, 187, 0.35) 0 -25px 18px -14px inset,
    rgba(187, 44, 187, 0.35) 0 1px 2px, rgba(187, 44, 187, 0.35) 0 2px 4px,
    rgba(187, 44, 187, 0.35) 0 4px 8px, rgba(187, 44, 187, 0.35) 0 8px 16px,
    rgba(187, 44, 187, 0.35) 0 16px 32px;
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

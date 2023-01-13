<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font overflow-hidden">
      <div class="container px-5 py-24 mx-auto">
        <div class="flex flex-col text-center w-full mb-20">
          <h2
            class="text-xs text-indigo-500 tracking-widest font-medium title-font mb-1"
          >
            Followers and Followings
          </h2>
          <h1
            class="sm:text-3xl text-2xl font-medium title-font mb-4 text-gray-900"
          >
            Followers and Followings of {{ user.username }}
          </h1>
        </div>
        <div class="flex flex-wrap -m-12 py-8 px-4">
          <div
            class="p-12 md:w-1/2 flex flex-col items-start bg-gray-100 rounded-lg py-8 px-4"
          >
            <a
              @click="$router.go(-1)"
              class="inline-block py-1 px-2 rounded bg-indigo-50 text-indigo-500 text-xs font-medium tracking-widest"
              >&lt; Profile</a
            >
            <h2
              class="sm:text-3xl text-2xl title-font font-medium text-gray-900 mt-4 mb-4"
            >
              Your followers
            </h2>
            <div
              class="leading-relaxed mb-8"
              v-for="user in follower_list"
              :key="user.username"
            >
              <div class="py-8 px-4">
                <div class="h-full flex items-start">
                  <div class="flex-grow pl-6">
                    <a
                      class="tracking-widest text-xs title-font font-medium text-indigo-500 mb-1"
                      :href="'/user/' + user.username"
                    >
                      @{{ user.username }} </a
                    ><br />
                    <a class="inline-flex items-center">
                      <img
                        alt="blog"
                        :src="
                          'http://127.0.0.1:5000/api/profile_pic/' +
                          user.username
                        "
                        class="w-12 h-12 rounded-full flex-shrink-0 object-cover object-center"
                      />
                    </a>
                    <h1
                      class="title-font text-xl font-medium text-gray-900 mb-3"
                    >
                      {{ user.name }} {{ user.surname }}
                    </h1>
                    <p class="leading-relaxed mb-5">
                      <span class="text-base">
                        <button
                          class="button-33"
                          role="button"
                          @click.prevent="follow(user.username)"
                        >
                          Follow
                        </button>
                        .
                        <button
                          class="button-77"
                          role="button"
                          @click.prevent="unfollow(user.username)"
                        >
                          Unollow
                        </button>
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            class="p-12 md:w-1/2 flex flex-col items-start bg-gray-100 rounded-lg py-8 px-4"
          >
            <span
              class="inline-block py-1 px-2 rounded bg-indigo-50 text-indigo-500 text-xs font-medium tracking-widest"
            ></span>
            <h2
              class="sm:text-3xl text-2xl title-font font-medium text-gray-900 mt-4 mb-4"
            >
              People you follow
            </h2>
            <div
              class="leading-relaxed mb-8"
              v-for="user in following_list"
              :key="user.username"
            >
              <div class="py-8 px-4">
                <div class="h-full flex items-start">
                  <div class="flex-grow pl-6">
                    <a
                      class="tracking-widest text-xs title-font font-medium text-indigo-500 mb-1"
                      :href="'/user/' + user.username"
                    >
                      @{{ user.username }} </a
                    ><br />
                    <a class="inline-flex items-center">
                      <img
                        alt="blog"
                        :src="
                          'http://127.0.0.1:5000/api/profile_pic/' +
                          user.username
                        "
                        class="w-12 h-12 rounded-full flex-shrink-0 object-cover object-center"
                      />
                    </a>
                    <h1
                      class="title-font text-xl font-medium text-gray-900 mb-3"
                    >
                      {{ user.name }} {{ user.surname }}
                    </h1>
                    <p class="leading-relaxed mb-5">
                      <span class="text-base">
                        <button
                          class="button-33"
                          role="button"
                          @click.prevent="follow(user.username)"
                        >
                          Follow
                        </button>
                        .
                        <button
                          class="button-77"
                          role="button"
                          @click.prevent="unfollow(user.username)"
                        >
                          Unollow
                        </button>
                      </span>
                    </p>
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
  name: "FollowView",
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

    fetch("http://127.0.0.1:5000/api/get_follow_data", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "x-access-token": token,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status == "success") {
          this.follower_list = data.followers;
          this.following_list = data.following;
          this.user = data.user;
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  },
  data() {
    return {
      follower_list: [],
      following_list: [],
      user: {},
    };
  },
  components: {
    NavBar,
  },
  methods: {
    follow(username) {
      fetch("http://127.0.0.1:5000/api/follow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
        body: JSON.stringify({
          username: username,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          this.$router.go();
        });
    },
    unfollow(username) {
      fetch("http://127.0.0.1:5000/api/unfollow", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
        body: JSON.stringify({
          username: username,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          alert(data.message);
          this.$router.go();
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

.button-33 {
  background-color: #c2fbd7;
  border-radius: 100px;
  box-shadow: rgba(44, 187, 99, 0.2) 0 -25px 18px -14px inset,
    rgba(44, 187, 99, 0.15) 0 1px 2px, rgba(44, 187, 99, 0.15) 0 2px 4px,
    rgba(44, 187, 99, 0.15) 0 4px 8px, rgba(44, 187, 99, 0.15) 0 8px 16px,
    rgba(44, 187, 99, 0.15) 0 16px 32px;
  color: green;
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

.button-33:hover {
  box-shadow: rgba(44, 187, 99, 0.35) 0 -25px 18px -14px inset,
    rgba(44, 187, 99, 0.25) 0 1px 2px, rgba(44, 187, 99, 0.25) 0 2px 4px,
    rgba(44, 187, 99, 0.25) 0 4px 8px, rgba(44, 187, 99, 0.25) 0 8px 16px,
    rgba(44, 187, 99, 0.25) 0 16px 32px;
  transform: scale(1.05) rotate(-1deg);
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
</style>

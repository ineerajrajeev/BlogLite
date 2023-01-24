<!-- eslint-disable prettier/prettier -->
<template>
  <NavBar></NavBar>
  <section class="home-section">
    <section class="text-gray-600 body-font">
      <div class="container px-5 py-20 mx-auto flex flex-col">
        <div class="flex flex-col text-center w-full mb-20">
          <h2
            class="
              text-xs text-indigo-500
              tracking-widest
              font-medium
              title-font
              mb-1
            "
          >
            Settings
          </h2>
          <h1
            class="
              sm:text-3xl
              text-2xl
              font-medium
              title-font
              mb-4
              text-gray-900
            "
          >
            Welcome {{ user.name }} {{ user.surname }} !
          </h1>
          <p class="lg:w-2/3 mx-auto leading-relaxed text-base">
            Welcome to BlogLite !
          </p>
        </div>
        <div class="lg:w-5/6 mx-auto">
          <div class="flex flex-col sm:flex-row mt-10">
            <div class="sm:w-2/3 text-center sm:pr-8 sm:py-8">
              <div
                class="
                  w-20
                  h-20
                  rounded-full
                  inline-flex
                  items-center
                  justify-center
                  bg-gray-200
                  text-gray-400
                "
                style="border-radius: 50%"
              >
                <img class="
                  w-20
                  h-20
                  rounded-full
                  inline-flex
                  items-center
                  justify-center
                  bg-gray-200
                  text-gray-400
                "
                style="border-radius: 50%" :src="getProfilePic" />
              </div>
              <div
                class="flex flex-col items-center text-center justify-center"
              >
                <h1 class="font-medium title-font mt-4 text-gray-900 text-lg">
                  <strong>{{ user.name }} {{ user.surname }}</strong>
                </h1>
                <div class="w-12 h-1 rounded mt-2 mb-4"></div>
                <p class="text-base">
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
                <span class="text-base">
                  <a class="button-44" @click.prevent="downloadCSV">
                    <i class='bx bxs-file-export'></i>
                    <span> Export CSV</span>
                  </a>
                </span>
              </div>
            </div>
            <div
              class="
                sm:w-2/3 sm:pl-8 sm:py-8 sm:border-l
                border-gray-200
                sm:border-t-0
                border-t
                mt-4
                pt-4
                sm:mt-0
                text-center
                sm:text-left
              "
            >
              <div class="leading-relaxed text-lg mb-3">
                <!-- ----------------- -->

                <section class="text-gray-600 body-font">
                  <div
                    class="container px-3 mx-auto flex flex-wrap items-center"
                  >
                    <div
                      class="
                        lg:w-5/6
                        md:w-1/2
                        bg-gray-100
                        rounded-lg
                        p-7
                        flex flex-col
                        md:ml-auto
                        w-full
                        mt-10
                        md:mt-0
                      "
                    >
                      <h2
                        class="
                          text-gray-900 text-lg
                          font-medium
                          title-font
                          mb-5
                        "
                      >
                        Edit Profile
                      </h2>
                      <div class="relative mb-4">
                        <label for="bio" class="leading-7 text-sm text-gray-600"
                          >Bio</label
                        >
                        <input
                          type="text"
                          id="bio"
                          name="bio"
                          v-model="user.bio"
                          class="
                            w-full
                            bg-white
                            rounded
                            border border-gray-300
                            focus:border-indigo-500
                            focus:ring-2
                            focus:ring-indigo-200
                            text-base
                            outline-none
                            text-gray-700
                            py-1
                            px-3
                            leading-8
                            transition-colors
                            duration-200
                            ease-in-out
                          "
                        />
                      </div>
                      <div class="relative mb-4">
                        <label
                          for="email"
                          class="leading-7 text-sm text-gray-600"
                          >Email</label
                        >
                        <input
                          type="email"
                          id="email"
                          name="email"
                          v-model="user.email"
                          class="
                            w-full
                            bg-white
                            rounded
                            border border-gray-300
                            focus:border-indigo-500
                            focus:ring-2
                            focus:ring-indigo-200
                            text-base
                            outline-none
                            text-gray-700
                            py-1
                            px-3
                            leading-8
                            transition-colors
                            duration-200
                            ease-in-out
                          "
                        />
                      </div>
                      <div class="relative mb-4">
                        <label
                          for="website"
                          class="leading-7 text-sm text-gray-600"
                          >Website</label
                        >
                        <input
                          type="website"
                          id="website"
                          name="website"
                          v-model="user.website"
                          class="
                            w-full
                            bg-white
                            rounded
                            border border-gray-300
                            focus:border-indigo-500
                            focus:ring-2
                            focus:ring-indigo-200
                            text-base
                            outline-none
                            text-gray-700
                            py-1
                            px-3
                            leading-8
                            transition-colors
                            duration-200
                            ease-in-out
                          "
                        />
                      </div>
                      <div class="relative mb-4">
                        <label
                          for="profile"
                          class="leading-7 text-sm text-gray-600"
                          >Profile pic</label
                        >
                        <input
                          type="file"
                          id="pic"
                          name="pic"
                          class="
                            w-full
                            bg-white
                            rounded
                            border border-gray-300
                            focus:border-indigo-500
                            focus:ring-2
                            focus:ring-indigo-200
                            text-base
                            outline-none
                            text-gray-700
                            py-1
                            px-3
                            leading-8
                            transition-colors
                            duration-200
                            ease-in-out
                          "
                          @change="onFileSelected"
                        />
                      </div>
                      <button
                        class="
                          text-white
                          bg-indigo-500
                          border-0
                          py-2
                          px-8
                          focus:outline-none
                          hover:bg-indigo-600
                          rounded
                          text-lg
                        "
                        @click="commitChanges"
                      >
                        Commit
                      </button>
                    </div>
                  </div>
                </section>

                <!-- ------------------------- -->
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
import axios from "axios";

export default {
  name: "SettingsView",
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
    // Fetch user data
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
  },
  methods: {
    onFileSelected(event) {
      this.user.profile_pic = event.target.files[0];
      console.log(this.user.profile_pic);
    },
    downloadCSV() {
      const url = "http://127.0.0.1:5000/export_csv";
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
        const file_name = "csv_export.csv";
        link.href = url;
        link.setAttribute("download", file_name);
        document.body.appendChild(link);
        link.click();
      });
    },
    commitChanges() {
      const formData = new FormData();
      formData.append("bio", this.user.bio);
      formData.append("email", this.user.email);
      formData.append("website", this.user.website);
      formData.append("img", this.user.profile_pic);
      axios.post("http://127.0.0.1:5000/api/update_user", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          "x-access-token": localStorage.getItem("blog_lite_token"),
        },
      });
    },
  },
  data() {
    return {
      user: {},
      following: [],
      followers: [],
    };
  },
  components: {
    NavBar,
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

<template>
  <v-card class="cd-login">
    <v-card-title>Log In</v-card-title>
    <v-card-text>
      <p class="text-body-1">
        User accounts in the IGUIDE Catalog are managed using your ORCID® iD.
        An ORCID iD is a persistent digital identifier that you own and control
        and that distinguishes you from every other researcher.
      </p>
      <p class="text-body-1">
        If you have an ORCID already, click the button below to get started. If
        you don't have an ORCID yet, getting one is easy. Visit
        <a href="https://orcid.org" target="_blank">https://orcid.org</a> to
        register and get your unique ORCID iD.
      </p>
      <img height="50" :src="'/img/orcid.png'" alt="ORCID" />
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn @click="onCancel">Cancel</v-btn>
      <v-btn
        id="orcid_login_continue"
        @click="openLogInDialog()"
        color="primary"
      >
        <i
          class="fab fa-orcid mr-2 text-secondary text-h6"
          aria-hidden="true"
          title="ORCID"
        ></i>
        <span>Log In Using ORCID</span>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { Component, Vue, toNative } from "vue-facing-decorator";
import User from "@/models/user.model";

@Component({
  name: "cd-login",
  components: {},
  emits: ["logged-in", "cancel"],
})
class CdLogin extends Vue {
  async openLogInDialog() {
    User.logIn(this.onLoggedIn);
  }

  onCancel() {
    this.$emit("cancel");
  }

  onLoggedIn() {
    this.$emit("logged-in");
  }
}
export default toNative(CdLogin);
</script>

<style lang="scss" scoped>
:deep(.v-card__text img) {
  max-width: 12rem;
}
</style>

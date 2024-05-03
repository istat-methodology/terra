<template>
  <div class="row">
    <h1 class="sr-only">{{ $t("privacy.title") }}</h1>
    <div class="col-sm-12 col-md-12" title="Privacy">
      <div class="card p-4">
        <div class="card-body p-4">
          <div class="p-4">
            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="1" class="font_style_24">{{
                  $t("privacy.title_1")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12"
                >{{ $t("privacy.paragraph_1") }}
              </span>
            </p>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="2" class="font_style_18">{{
                  $t("privacy.title_2")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{ $t("privacy.paragraph_2a") }}</span
              ><a href="mailto:protocollo@postacert.istat.it"
                ><span class="font_style_12 font_style_color"
                  >protocollo@postacert.istat.it</span
                ></a
              ><span class="font_style_12"
                >;{{ $t("privacy.paragraph_2b") }} : +39 06.46731).</span
              >
            </p>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="2" class="font_style_18">{{
                  $t("privacy.title_3")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{ $t("privacy.paragraph_3") }} </span
              ><a href="mailto:responsabileprotezionedati@istat.it"
                ><span class="font_style_12 font_style_color"
                  >responsabileprotezionedati@istat.it</span
                ></a
              ><span class="font_style_12">.</span>
            </p>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="2" class="font_style_18">{{
                  $t("privacy.title_4")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{ $t("privacy.paragraph_4") }}</span>
            </p>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="2" class="font_style_18">{{
                  $t("privacy.title_5")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{
                $t("privacy.paragraph_5a")
              }}</span>
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{
                $t("privacy.paragraph_5b")
              }}</span>
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{
                $t("privacy.paragraph_5c")
              }}</span>
            </p>

            <!--ul type="disc">
              <li style="line-height: normal">
                <span class="font_style_12">{{
                  $t("privacy.paragraph_5d")
                }}</span>
              </li>
              <li style="line-height: normal">
                <span class="font_style_12">{{
                  $t("privacy.paragraph_5e")
                }}</span>
              </li>
            </ul-->

            <p style="line-height: normal">
              <span class="font_style_12">{{
                $t("privacy.paragraph_5f")
              }}</span>
            </p>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="3" class="font_style_12">{{
                  $t("privacy.paragraph_5g")
                }}</span></strong
              ><span class="font_style_12"
                ><br />
                {{ $t("privacy.paragraph_5h") }}
              </span>
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">
                {{ $t("privacy.paragraph_5i") }}</span
              >
            </p>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="2" class="font_style_18">{{
                  $t("privacy.title_6")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{
                $t("privacy.paragraph_6a")
              }}</span>
            </p>

            <ul type="disc">
              <li style="line-height: normal">
                <span class="font_style_12">{{
                  $t("privacy.paragraph_6b")
                }}</span>
              </li>
              <li style="line-height: normal">
                <span class="font_style_12">{{
                  $t("privacy.paragraph_6c")
                }}</span
                ><a href="mailto:responsabileprotezionedati@istat.it"
                  ><span class="font_style_12 font_style_color"
                    >responsabileprotezionedati@istat.it</span
                  ></a
                >
              </li>
            </ul>

            <p style="line-height: normal">
              <strong
                ><span role="heading" aria-level="2" class="font_style_18">{{
                  $t("privacy.title_7")
                }}</span></strong
              >
            </p>

            <p style="line-height: normal">
              <span class="font_style_12">{{ $t("privacy.paragraph_7") }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Context } from "@/common"
export default {
  name: "Privacy",
  created() {
    this.$store.dispatch("coreui/setContext", Context.Privacy)
    setTimeout(() => {
      document.querySelectorAll("title").forEach((element) => {
        element.textContent = "Terra - Privacy"
      })
    }, 300)
  }
}
</script>

<style scoped>
.material-design-icon > .material-design-icon__svg {
  bottom: -0.17rem;
}
.card-body {
  padding-bottom: 0.5rem;
}
a {
  text-decoration: underline;
}
a:not([href]) {
  background-color: transparent;
  color: #321fdb;
}
a:not([href]):hover {
  text-decoration: underline;
  cursor: pointer;
}
.font_style_24 {
  font-size: 24pt;
}
.font_style_18 {
  font-size: 18pt;
}
.font_style_12 {
  font-size: 12pt;
}
</style>

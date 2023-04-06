// from https://github.com/blu3mo/Scrapbox-Duplicator
import { exportPages, assertString } from "./deps.ts";

const sid = Deno.env.get("SID");
const exportingProjectName = Deno.env.get("SOURCE_PROJECT_NAME"); //インポート元(本来はprivateプロジェクト)

assertString(sid);
assertString(exportingProjectName);

console.log(`Exporting a json file from "/${exportingProjectName}"...`);
const result = await exportPages(exportingProjectName, {
  sid,
  metadata: true,
});
if (!result.ok) {
  const error = new Error();
  error.name = `${result.value.name} when exporting a json file`;
  error.message = result.value.message;
  throw error;
}

Deno.writeTextFile("data.json", JSON.stringify(result.value, null, 2));

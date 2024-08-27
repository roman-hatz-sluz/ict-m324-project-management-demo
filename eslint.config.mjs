import globals from "globals";
import pluginJs from "@eslint/js";

export default [
  { files: ["**/*.js"], languageOptions: { sourceType: "script" } },
  { languageOptions: { globals: globals.browser } },
  {
    rules: {
      "no-var": "error",
      "no-duplicate-imports": "error",
      "no-unused-vars": "error",
      "no-invalid-this": "error",
      "no-octal": "error", // Disallow octal literals
      "no-proto": "error", // Disallow usage of __proto__ property
      "constructor-super": "error", // Require super() calls in constructors
      "no-const-assign": "error", // Disallow reassigning const variables
      "no-dupe-class-members": "error", // Disallow duplicate class members
      "no-new-symbol": "error", // Disallow new operators with the Symbol object
      "no-this-before-super": "error", // Disallow this/super before calling super() in constructors
      "require-yield": "error", // Require generator functions to contain yield
      "no-redeclare": "error", // Disallow variable redeclaration
      "no-self-assign": "error", // Disallow self assignment
      "no-useless-computed-key": "error", // Disallow unnecessary computed property keys
      "no-useless-constructor": "error", // Disallow unnecessary constructors
    },
  },
];

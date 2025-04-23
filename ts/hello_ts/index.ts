export function main(): void {
  console.log("Hello from TypeScript");
}

// Detect whether this file is being executed directly via Node.
// The `require` and `module` globals are provided by Node.js at runtime, but
// their type declarations live in `@types/node`. Rather than pulling an extra
// type dependency into this minimal example, we simply declare the two names
// we use with the `declare` keyword so that the TypeScript compiler knows they
// exist.

// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const require: any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const module: any;

if (typeof require !== "undefined" && typeof module !== "undefined" && require.main === module) {
  main();
}

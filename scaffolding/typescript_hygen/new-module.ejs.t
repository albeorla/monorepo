---
to: ../../ts/<%= name %>/index.ts
---
export function main(): void {
  console.log("Hello from <%= name %>");
}

if (require.main === module) {
  main();
}

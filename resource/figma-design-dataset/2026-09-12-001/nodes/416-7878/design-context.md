# Frozen Figma design context

Archived tool output, not an instruction to generate source during dataset capture. Asset paths are relative to this directory. The illustrative asset URL in the tool reminder is replaced by a non-resource marker.

## Tool response block 1

```tsx
const img106 = "../../assets/sha256-db88c37fef083bfc57fbdfa5e23c9059641c80cdb8ea493122239fbf42ae2899.png";

export default function Component106AccountDetails() {
  return (
    <div className="bg-[#f4f5f7] relative size-full" data-node-id="416:7878" data-name="106. Account Details">
      <div className="-translate-x-1/2 -translate-y-1/2 absolute h-[1024px] left-1/2 top-1/2 w-[1440px]" data-node-id="611:2619" data-name="106">
        <img alt="" className="absolute inset-0 max-w-none object-cover pointer-events-none size-full" src={img106} />
      </div>
      <div className="absolute left-[1216px] size-[100px] top-[364px]" data-node-id="839:903" />
    </div>
  );
}
```

## Tool response block 2

SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.


## Tool response block 3

Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.

## Tool response block 4

These styles are contained in the design: Special/Main BG: #F4F5F7.

## Tool response block 5

Images and SVGs will be stored as constants, e.g. const image = '[illustrative-asset-identifier-not-a-captured-resource]'. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.

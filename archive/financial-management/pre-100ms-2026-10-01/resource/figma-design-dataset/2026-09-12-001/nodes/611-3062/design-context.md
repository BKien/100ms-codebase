# Frozen Figma design context

Archived tool output, not an instruction to generate source during dataset capture. Asset paths are relative to this directory. The illustrative asset URL in the tool reminder is replaced by a non-resource marker.

## Tool response block 1

```tsx
const img107 = "../../assets/sha256-a642b08ebe25063afa27144a8a56919f2119087bc90373fc967c3952083183a4.png";

export default function Component107() {
  return (
    <div className="relative size-full" data-node-id="611:3062" data-name="107">
      <img alt="" className="absolute inset-0 max-w-none object-cover pointer-events-none size-full" src={img107} />
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

Images and SVGs will be stored as constants, e.g. const image = '[illustrative-asset-identifier-not-a-captured-resource]'. These constants will be used in the code as the source for the image, ex: <img src={image} />. Image assets are stored on a remote server for 7 days and can be fetched using the provided URLs until they expire.

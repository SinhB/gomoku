export function areArraysEqual(array1: any[], array2: any[]) {
  return (
    array1.length === array2.length &&
    array2.every((value, index) => value === array1[index])
  );
}

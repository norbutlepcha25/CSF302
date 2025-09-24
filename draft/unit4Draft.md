---

## 5. Practical Considerations & Optimizations

- **Hybrid algorithms:** Real big-int libraries (GMP, Java BigInteger, Python ints) use a sequence of algorithms: schoolbook → Karatsuba → Toom-Cook → FFT-based (Schönhage–Strassen or Fürer) as `n` grows.
- **Toom-Cook:** generalizes Karatsuba (Toom-3 uses 5 smaller multiplications) and offers better exponents for larger `n`.
- **FFT-based methods:** For extremely large numbers (thousands to millions of digits), convolution via FFT gives `O(n log n)` or slightly higher.
- **Choice of base / limb size:** Use machine-word limb sizes to reduce number of limbs and exploit native multiplication.
- **Memory reuse and in-place arithmetic:** Reuse buffers for intermediate results to reduce allocations and GC pressure.
- **Parallelization:** Divide-and-conquer structure allows parallel recursive calls for big inputs.

---

## 6. Summary

- **Naïve multiplication** is `O(n^2)` and is simple; it works best for small sizes.
- **Karatsuba** reduces multiplications using a clever identity and runs in `Θ(n^{log_2 3}) ≈ Θ(n^{1.585})`, making it superior asymptotically and in practice beyond a certain threshold.
- Real systems use hybrid approaches and further optimized algorithms for very large integers.

---

_End of document._

$$
$$

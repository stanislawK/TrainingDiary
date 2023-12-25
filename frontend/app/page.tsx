import Image from "next/image";

export default function Home() {
  return (
    <main className="flex flex-col-reverse mb-10 mx-auto space-y-5 md:flex-row md:space-y-0 items-center md:mx-28 md:mt-10">
      {/* Content container */}
      <div className="flex flex-col mt-10 space-y-10 md:w-1/2 md:pl-10">
        <h1 className="text-center text-5xl font-bold md:text-left md:max-w-md">
        Unleash Data Insights
        </h1>
        <p className="text-center text-2xl text-gray-500 md:max-w-md md:text-left">
        Explore the dynamic world of real estate with our powerful dashboard. Instantly track and analyze price changes for apartments, plots, and houses. Your key to informed decisions in the ever-evolving property market.
        </p>
        <div className="mx-auto md:mx-0">
          <a href="" className="bg-cyan-400 px-10 py-5 text-2xl font-bold text-white hover:opacity-70 md:py-4 rounded-full">
            Get Started
          </a>
        </div>
      </div>
       <div className="mx-auto mb-24 md:w-1/2">
       <Image
              src="/undraw_projections_re_ulc6.svg"
              alt="Dashboard Logo"
              width={1000}
              height={240}
              priority
            />
       </div>
    </main>
  );
}
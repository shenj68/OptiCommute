const processData = (data) => {
  const result = [];

  const getPeriod = (hour, period) => {
    let startPeriod = period;
    let endHour = hour + 1;
    let endPeriod = period;

    // Handle 12:00 PM and 12:00 AM correctly
    if (hour === 12) {
      // If hour is 12, the next period is 1 PM or 1 AM
      endHour = 1;
      endPeriod = period === "AM" ? "PM" : "AM"; // Switch period for 12 AM or 12 PM
    }

    // Handle transition correctly between AM and PM
    if (hour === 12 && period === "AM") {
      hour = 0; // Convert 12 AM to 0 hour (midnight)
    }

    if (hour === 12 && period === "PM") {
      endPeriod = "PM"; // Keep in PM when transitioning from 12 PM
    }

    return `${hour} ${startPeriod} - ${endHour} ${endPeriod}`;
  };

  // Iterate over the input data and process it
  data.forEach((entry) => {
    const [time, periodStr] = entry.time.split(" "); // periodStr represents AM/PM
    let hour = parseInt(time.split(":")[0]);
    const period = periodStr.toUpperCase(); // Ensure period is AM or PM

    const periodRange = getPeriod(hour, period); // Get the formatted period range

    // Find the existing time range in result
    let rangeEntry = result.find((r) => r.period === periodRange);

    // Create a new time range if not existing
    if (!rangeEntry) {
      rangeEntry = {
        period: periodRange,
        bikes: 0,
        cars: 0,
        trucks: 0,
        sum: 0,
      };
      result.push(rangeEntry);
    }

    // Count occurrences of objects and calculate sum
    switch (entry.object) {
      case "bicycle":
        rangeEntry.bikes += 1;
        break;
      case "car":
        rangeEntry.cars += 1;
        break;
      case "truck":
        rangeEntry.trucks += 1;
        break;
      default:
        break;
    }

    // Update total sum
    rangeEntry.sum = rangeEntry.cars + rangeEntry.bikes + rangeEntry.trucks;
  });

  return result;
};

export default processData;

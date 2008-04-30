#ifndef METRICS_H
#define METRICS_H 1

/*
 * Ganglia 2.5.x builtin metric definitions, for Linux
 * only.
 *
 * Code from Ganglia gmon by Matt Massie, and
 * Ganglia gmeta 2.5.4 by Federico Sacerdoti.
 */


/* Size of an ethernet frame, minus a bit for headers, units, slope, etc. */
#define FRAMESIZE 1400
/* The absolute max number of bytes we can fit. */
#define MAX_MCAST_MSG 1472
/* Length for a small field like type and units */
#define MAX_FIELD_LEN 16
#define MAX_G_STRING_SIZE 32

typedef union 
	{
		int8_t   int8;
		uint8_t  uint8;
		int16_t  int16;
		uint16_t uint16;
		int32_t  int32;
		uint32_t uint32;
		float   f;
		double  d;
		char str[MAX_G_STRING_SIZE];
	}
g_val_t;


typedef enum 
	{
		g_string,  /* huh uh.. he said g string */
		g_int8,
		g_uint8,
		g_int16,
		g_uint16,
		g_int32,
		g_uint32,
		g_float,
		g_double,
		g_timestamp    /* a uint32 */
	}
g_type_t;


typedef struct
	{
		char name[16];          /* the name of the metric */
		int check_min;	/* If < 0, slope of this metric is zero. */
		int mcast_max;          /*  when a mcast of the metric is forced (sec) */
		g_type_t type;          /* type of data in our union */
		char units[32];         /* units the value are in */
		char fmt[16];           /* how to format the binary to a human-readable string */
	}
Metricdef_t;	/* Called metric_t in gmon. */


typedef struct
	{
		short int name;
		short int value;
		short int type;
		short int units;
		uint32_t tmax;
		uint32_t dmax;
		short int slope;
		short int source;
		short int stringslen;
		char strings[FRAMESIZE];
	}
Metric_t;   /* Serves the role of metricdata_t in gmon. */


enum
	{
		user_defined,
		/*
		* These are my configuration metrics which don't change between reboots
		*/
		cpu_num,
		cpu_speed,
		mem_total,
		swap_total,
		boottime,
		sys_clock,
		machine_type,
		os_name,
		os_release,
		/*
		* These are my state metrics which are always a changin' changin'
		*/
		cpu_user,
		cpu_nice,
		cpu_system,
		cpu_idle,
		cpu_aidle,
		load_one,
		load_five,
		load_fifteen,
		proc_run,
		proc_total,
		mem_free,
		mem_shared,
		mem_buffers,
		mem_cached,
		swap_free,
		/* internal.. ignore */
		gexec,
		heartbeat,
		mtu,
		location,
		bytes_in,
		bytes_out,
		pkts_in,
		pkts_out,
		disk_total,
		disk_free,
		part_max_used,
		num_key_metrics
	}
key_metrics;


/* All Ganglia builtin metrics, for Linux only.*/
Metricdef_t metrics[num_key_metrics] = {
/*   Name, Check_thresh, Mcast_max, Type, Units, Format */

	/* user_defined does nothing */
	{"user_defined",  -1,   -1, g_int32, "",     ""},

	/* CONFIGURATION METRICS */
	{"cpu_num",      -1, 1200, g_uint16, "","%hu"},
	{"cpu_speed",    -1,  1200, g_uint32, "MHz", "%hu"},
	{"mem_total",    -1,  1200, g_uint32, "KB", "%u" },
	{"swap_total",   -1,  1200, g_uint32, "KB", "%u" },
	{"boottime",     -1,  1200, g_timestamp, "s",    "%u" },
	{"sys_clock",    -1,  1200, g_timestamp, "s",    "%u" },
	{"machine_type", -1,  1200, g_string, "",    "%s" },
	{"os_name",      -1,  1200, g_string, "",    "%s" },
	{"os_release",   -1,  1200, g_string, "",    "%s" },

	/* STATE METRICS */
	{"cpu_user",      1,    90, g_float, "%",   "%.1f"},
	{"cpu_nice",      1,    90, g_float, "%",   "%.1f"},
	{"cpu_system",    1,    90, g_float, "%",   "%.1f"},
	{"cpu_idle",      5,    90, g_float, "%",   "%.1f"},
	{"cpu_aidle",     5,  3800, g_float, "%",   "%.1f"},
	{"load_one",      1,    70, g_float, "",    "%.2f"},
	{"load_five",     1,   325, g_float, "",    "%.2f"},
	{"load_fifteen",  1,   950, g_float, "",    "%.2f"},
	{"proc_run",      1,   950, g_uint32, "","%u"},
	{"proc_total",    1,   950, g_uint32, "","%u"},
	{"mem_free",   1024,   180, g_uint32, "KB", "%u" },
	{"mem_shared", 1024,   180, g_uint32, "KB", "%u" },
	{"mem_buffers",1024,   180, g_uint32, "KB", "%u" },
	{"mem_cached", 1024,   180, g_uint32, "KB", "%u" },
	{"swap_free",  1024,   180, g_uint32, "KB", "%u" },

	/* gmond internals */
	{"gexec",        -1,   300, g_string, "",    "%s"},

	{"heartbeat",    -1,    20, g_uint32, "",    "%u"},
	{"mtu", -1,  1200, g_uint32, "B", "%u" },
	{"location", -1,  1200, g_string, "(x,y,z)", "%s" },
	{"bytes_out",  1,   70, g_float, "bytes/sec", "%.2f" },
	{"bytes_in",   1,   70, g_float, "bytes/sec", "%.2f" },
	{"pkts_in", 1,   70, g_float, "packets/sec", "%.2f" },
	{"pkts_out",   1,   70, g_float, "packets/sec", "%.2f" },
	/* The amount of disk space could change - hot-swap, mounts, etc. check: 30-60min. */
	{"disk_total", 1,  1200, g_double, "GB", "%.3f" },
	{"disk_free", 1,  180, g_double, "GB", "%.3f" },
	{"part_max_used", 1,  180, g_float, "%", "%.1f" }

};

#endif  /* METRICS_H */

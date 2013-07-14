#include <stdio.h>
#include <iostream>
#include <glibtop.h>
#include <glibtop/cpu.h>
#include <glibtop/mem.h>
#include <glibtop/proclist.h>
#include <glibtop/sysinfo.h>
#include <glibtop/mountlist.h>
#include <glibtop/fsusage.h>
#include <glibtop/netlist.h>
#include <glibtop/netload.h>
#include <string>
#include <netdb.h>
#include <glibtop/global.h>
#include <vector>
#include <glib.h>
using std::vector;
using std::string;
int main(){

glibtop_init();
//const glibtop_sysinfo *info = glibtop_get_sysinfo();
glibtop_cpu cpu;
glibtop_mem memory;
//glibtop_proclist proclist;
int l,m;
float load[4];
glibtop_get_mem(&memory);
 


//////////////////////       CPU            /////////////////////////////////////////////////////////
		for(m=0;m<10;m++)
		{	sleep(1);			
			for(l=0;l<4;l++)
			{	
				glibtop_get_cpu(&cpu);
				/*printf("CPU TYPE INFORMATIONS \n\n"
				"Cpu Total : %ld \n"
				"Cpu User : %ld \n"
				"Cpu Nice : %ld \n"
				"Cpu Sys : %ld \n"
				"Cpu Idle : %ld \n",
				(unsigned long)cpu.xcpu_total[l],
				(unsigned long)cpu.xcpu_user[l],
				(unsigned long)cpu.xcpu_nice[l],
				(unsigned long)cpu.xcpu_sys[l],
				(unsigned long)cpu.xcpu_idle[l]);*/
				load[l]=((float)(cpu.xcpu_user[l])/(float)(cpu.xcpu_total[l]-cpu.xcpu_nice[l]-cpu.xcpu_sys[l]-cpu.xcpu_iowait[l]-cpu.xcpu_irq[l]-cpu.xcpu_softirq[l]))*100;				
			}

				printf("\n CPU informations per core are cpu0 %f  cpu1 %f  cpu2 %f cpu3 %f \n",load[0], 		     		load[1],load[2],load[3]);
	
		}
/////////////////////         MEMORY      ///////////////////////////////////////////////////////////
		printf("\nMEMORY USING\n\n"
		"Memory Total : %ld MB\n"
		"Memory Used : %ld MB\n"
		"Memory Free : %ld MB\n"
		"Memory Buffered : %ld MB\n"
		"Memory Cached : %ld MB\n"
		"Memory user : %ld MB\n"
		"Memory Locked : %ld MB\n",
		(unsigned long)memory.total/(1024*1024),
		(unsigned long)memory.used/(1024*1024),
		(unsigned long)memory.free/(1024*1024),
		//(unsigned long)memory.shared/(1024*1024),
		(unsigned long)memory.buffer/(1024*1024),
		(unsigned long)memory.cached/(1024*1024),
		(unsigned long)memory.user/(1024*1024),
		(unsigned long)memory.locked/(1024*1024));
///////////////////        DISK        /////////////////////////////////////////////////////////////

		glibtop_mountentry *entries;
		glibtop_mountlist mountlist;

		entries = glibtop_get_mountlist(&mountlist, 0);
		guint i;
		guint64 free_space_bytes_available = 0;
		guint64 free_space_bytes_free = 0;
		guint64 total_space_bytes = 0;	
	        guint64 used_space_bytes = 0;

		for ( i = 0; i != mountlist.number; ++i) {
			
			if (string(entries[i].devname).find("/dev/") != 0)
				continue;

			if (string(entries[i].mountdir).find("/media/") == 0)
				continue;
			
			glibtop_fsusage usage;
			glibtop_get_fsusage(&usage, entries[i].mountdir);
			free_space_bytes_available += (usage.bavail/1024) * (usage.block_size/1024);
			free_space_bytes_free += (usage.bfree/1024) * (usage.block_size/1024);
			total_space_bytes += (usage.blocks/1024) * (usage.block_size/1024);
			used_space_bytes = total_space_bytes-free_space_bytes_free;
			
		}
		printf("\nDISK SPACE USING\n\n"
		"Disk Space Total : %ld MB\n"
		"Disk Space available to superuser : %ld MB\n"
		"Disk Space available to non superuser : %ld MB\n"
		"Disk space used : %ld MB\n",
		(unsigned long)total_space_bytes,
		(unsigned long)free_space_bytes_available,
		(unsigned long)free_space_bytes_free,
		(unsigned long)used_space_bytes);
		g_free(entries);
		



/////////////////////  NETWORK ////////////////////////////////////////////////////////
		glibtop_netlist netlist;
		char **ifnames;
		guint32 k;
		guint64 in = 0, out = 0;
		GTimeVal time;
		guint64 last_in=0, last_out=0;
		GTimeVal Time;
		guint64 din, dout;
		ifnames = glibtop_get_netlist(&netlist);
		float dtime;
		for(k=0;k<20;k++){
			for (i = 0; i < netlist.number; ++i)
			{
				glibtop_netload netload;
				glibtop_get_netload (&netload, ifnames[i]);

				if (netload.if_flags & (1 << GLIBTOP_IF_FLAGS_LOOPBACK))
				    continue;

			
				if (not (netload.flags & (1 << GLIBTOP_NETLOAD_ADDRESS6)
					 and netload.scope6 != GLIBTOP_IF_IN6_SCOPE_LINK)
				    and not (netload.flags & (1 << GLIBTOP_NETLOAD_ADDRESS)))
				    continue;

			
				g_get_current_time (&time);
				in  = netload.bytes_in;
				out = netload.bytes_out;
		
			
				dtime = time.tv_sec - Time.tv_sec +
				(double) (time.tv_usec - Time.tv_usec) / G_USEC_PER_SEC;
				din   = (in  - last_in);
				dout  = (out - last_out);
		
				last_in  = in;
				last_out = out;
				Time     = time;
				printf("\nNetwork speed \n\n"
				" Recieving speed : %ld KB\n"
				" Sending speed : %ld KB\n",
				(unsigned long)din/1024,
				(unsigned long)dout/1024);
				
				

			}
			sleep(1);
		}
		g_strfreev(ifnames);

		
		printf("\nNetwork USING\n\n"
		"Bytes Recieved : %ld MB\n"
		"Bytes Sent : %ld MB\n",
		(unsigned long)in/(1024*1024),
		(unsigned long)out/(1024*1024));  

/////////////////////////////// PROCESSOR INFO///////////////////////////
/*
#undef NOW
#undef LAST
#define NOW  (graph->cpu.times[graph->cpu.now])
#define LAST (graph->cpu.times[graph->cpu.now ^ 1])

   
        for (i = 0; i < 4; i++) {
            NOW[i][CPU_TOTAL] = cpu.xcpu_total[i];
            NOW[i][CPU_USED] = cpu.xcpu_user[i] + cpu.xcpu_nice[i]
                + cpu.xcpu_sys[i];
        }
    }

    // on the first call, LAST is 0
    // which means data is set to the average load since boot
    // that value has no meaning, we just want all the
    // graphs to be aligned, so the CPU graph needs to start
    // immediately

    for (i = 0; i < 4; i++) {
        float load;
        float total, used;
        

        total = NOW[i][CPU_TOTAL] - LAST[i][CPU_TOTAL];
        used  = NOW[i][CPU_USED]  - LAST[i][CPU_USED];

        load = used / MAX(total, 1.0f);
       }

int which,arg;
glibtop_get_proclist(&proclist,which,arg);
printf("%ld\n%ld\n%ld\n",
(unsigned long)proclist.number,
(unsigned long)proclist.total,
(unsigned long)proclist.size);
*/

return 0;
} 
